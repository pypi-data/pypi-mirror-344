use anyhow::{Context, Result};
use std::os::fd::AsFd;

use nix::{
    libc::_exit,
    unistd::{self, close, ForkResult},
};
use oxiida::{
    lang::{lex::LalrLexer, parser::parse_stmt, ast},
    runtime::{
        self,
        ffi::{CallMsg, CallSpec, FFIActor, FFIHandler},
        FilePersistence, PersistenceHandler, VarEnv,
    },
};
use pyo3::{
    exceptions::PyRuntimeError,
    ffi::{self, c_str},
    prelude::*,
    types::{PyDict, PyTuple},
};
use serde_pyobject::{from_pyobject, to_pyobject};
use tokio::sync::mpsc;

struct PyCallActor {
    receiver: mpsc::Receiver<CallMsg>,

    // The locals here need to be a `Send`, the PyDict is not Send.
    // Py<PyDict> is detached from GIL and can cross the thread boundary.
    // This make python functions can run natively by tokio multithreading with thread steal.
    locals: Py<PyDict>,
}

impl PyCallActor {
    fn new(locals: Py<PyDict>, rx: mpsc::Receiver<CallMsg>) -> Self {
        PyCallActor {
            receiver: rx,
            locals,
        }
    }
}

impl FFIActor for PyCallActor {
    async fn receive(&mut self) -> Option<CallMsg> {
        self.receiver.recv().await
    }

    fn handle_message(&self, msg: CallMsg) {
        // increment Py reference counter, clone must inside GIL
        let locals = Python::with_gil(|py| self.locals.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            match msg.ccmode {
                ast::ConcurrentMode::MP => {
                    match run_py_call_mp(&msg.payload, &locals) {
                        Ok(result) => {
                            // Ignoring send-errors is fine: it only happens if the caller
                            // already dropped the receiver.
                            let _ = msg.reply_to.send(result);
                        }
                        Err(err) => {
                            // XXX: if actor runs in daemon, the eprint will goes to logs there.
                            // How to have a nice way to make it easy to be noticed by the end user?
                            // I also need to think about the error value send back to the oxiida rt,
                            // how the runtime deal with it? How it downcast as an proper error type?
                            let _ = msg.reply_to.send(serde_json::json!(format!("{err}")));
                            eprintln!("python call except: {err}");
                            // FIXME: this drastic exit is not good it kill other processes.
                            // Better is send a structured error back and leave the run function to return
                            // an error.
                            std::process::exit(85)
                        }
                    }
                }
                ast::ConcurrentMode::MT => {
                    // TODO: find a way to detect it is a CPU bound function call and throw a notification
                    // to user at runtime to use MP to run or send to outer machine.
                    match run_py_call_mt(&msg.payload, &locals) {
                        Ok(result) => {
                            // Ignoring send-errors is fine: it only happens if the caller
                            // already dropped the receiver.
                            let _ = msg.reply_to.send(result);
                        }
                        Err(err) => {
                            let _ = msg.reply_to.send(serde_json::json!(format!("{err}")));
                            eprintln!("python call except: {err}");
                            // FIXME: this drastic exit is not good it kill other processes.
                            // Better is send a structured error back and leave the run function to return
                            // an error.
                            std::process::exit(85)
                        }
                    }
                },
            };
        });
    }
}

// a sync fn calls python function in a gil of spawn_blocking thread
fn run_py_call_mt(
    payload: &serde_json::Value,
    locals: &Py<PyDict>,
) -> anyhow::Result<serde_json::Value> {
    let payload = payload.clone();
    let spec: CallSpec =
        serde_json::from_value(payload).context("unable to convert payload to CallSpec")?;

    Python::with_gil(|py| {
        let func_name = spec.function;

        let func = if let Some(ref module) = spec.module {
            let module = py
                .import(module)
                .context(format!("unable to load module '{module}'"))?;
            module
                .getattr(&func_name)
                .context(format!("unable to load function '{}'", &func_name))?
        } else {
            let locals = locals.bind(py);
            match locals.get_item(&func_name)? {
                Some(func_name) => func_name,
                None => {
                    return Err(PyErr::new::<pyo3::exceptions::PyKeyError, _>(format!(
                        "function '{}' not found in locals",
                        &func_name
                    ))
                    .into());
                }
            }
        };

        let py_args: Vec<_> = spec
            .args
            .iter()
            .map(|v| to_pyobject(py, v))
            .collect::<Result<_, _>>()?;

        let py_args = PyTuple::new(py, &py_args)?;

        let py_result = func.call1(py_args).context("func call fail")?;
        // TODO: check and understand how this serde_pyobject crate works
        let json = from_pyobject(py_result).context("unable to convert result to json value")?;
        Ok(json)
    })
}

// XXX: require careful check since there are unsafe and buf r/w
fn run_py_call_mp(
    payload: &serde_json::Value,
    locals: &Py<PyDict>,
) -> anyhow::Result<serde_json::Value> {
    let spec: CallSpec =
        serde_json::from_value(payload.clone()).context("unable to convert payload to CallSpec")?;

    // OS pipe for result bytes (rd = parent side, wr = child side)
    let (rd, wr) = unistd::pipe().context("pipe() failed")?;

    let (func, py_args) = Python::with_gil(|py| -> anyhow::Result<(Py<PyAny>, Py<PyTuple>)> {
        let func_name = &spec.function;
        let func = if let Some(ref module) = spec.module {
            py.import(module)?.getattr(func_name)?
        } else {
            locals.bind(py).get_item(func_name)?.ok_or_else(|| {
                pyo3::exceptions::PyKeyError::new_err(format!(
                    "function '{func_name}' not found in locals"
                ))
            })?
        };

        let py_args: Vec<_> = spec
            .args
            .iter()
            .map(|v| to_pyobject(py, v))
            .collect::<Result<_, _>>()?;
        let tuple: Py<PyTuple> = PyTuple::new(py, &py_args)?.into();
        let func = func.into();
        Ok((func, tuple))
    })?;

    // when fork I should not hold gil
    match unsafe { unistd::fork() }.context("fork failed")? {
        ForkResult::Child => {
            // close parent's read-end
            close(rd).ok();

            // Re-enter Python **inside the child only**
            Python::with_gil(|py| -> anyhow::Result<_> {
                // re-initialise CPython locks that broke across fork
                // https://docs.python.org/3/c-api/sys.html#c.PyOS_AfterFork_Child
                unsafe { ffi::PyOS_AfterFork_Child() };

                let py_args = py_args.bind(py);
                let result = func.call1(py, py_args).context("func call failed")?;
                let result = result.bind(py).clone();
                let json_val: serde_json::Value =
                    from_pyobject(result).context("result to json failed")?;
                let json_bytes = serde_json::to_vec(&json_val)?;
                unistd::write(wr, &json_bytes).ok();
                Ok(())
            })?;
            unsafe { _exit(0) };
        }

        ForkResult::Parent { child: _ } => {
            close(wr).ok(); // parent only reads
            let mut buf = Vec::with_capacity(1024);
            let mut tmp = [0u8; 4096];
            loop {
                match unistd::read(rd.as_fd(), &mut tmp) {
                    Ok(0) => break, // EOF
                    Ok(n) => buf.extend_from_slice(&tmp[..n]),
                    Err(nix::errno::Errno::EINTR) => continue,
                    Err(e) => return Err(e.into()),
                }
            }
            close(rd).ok();

            // let _ = waitpid(child, None);
            let val: serde_json::Value =
                serde_json::from_slice(&buf).context("child returned invalid JSON")?;
            Ok(val)
        }
    }
}

#[pyfunction(signature = (workflow, locals = None))]
fn run<'py>(py: Python<'py>, workflow: &str, locals: Option<Bound<'py, PyDict>>) -> PyResult<()> {
    let py_locals: Py<PyDict> = {
        let gil_locals = match locals {
            Some(b) => b,
            None => py
                .eval(
                    c_str!("__import__('inspect').currentframe().f_back.f_locals"),
                    None,
                    None,
                )?
                .downcast_into::<PyDict>()?,
        };
        gil_locals.unbind() // make it a Py<PyDict>, to detach from GIL
    };
    // dbg!(py_locals);

    // avoid it become dangling when GIL dropped
    let workflow = workflow.to_owned();
    let py_varenv_set = py_locals
        .bind_borrowed(py)
        .keys()
        .iter()
        .filter_map(|key| key.extract::<String>().ok())
        .collect();

    // `run` is call from python therefore hold the GIL, but thread spawned
    // inside message handler also request for a GIL, but this thread never release it, deadlock.
    py.allow_threads(move || -> PyResult<_> {
        let rt = tokio::runtime::Builder::new_current_thread()
            .worker_threads(5)
            .enable_all()
            .build()
            .unwrap();

        // must goes before actors initialization where rt is needed to spawn tasks.
        let _guard = rt.enter();

        let lexer = LalrLexer::new(&workflow);
        let stmts =
            parse_stmt(lexer, &workflow).map_err(|err| PyRuntimeError::new_err(err.to_string()))?;

        let local_set = tokio::task::LocalSet::new();
        let mut glb_var_env = VarEnv::new(py_varenv_set);

        #[allow(clippy::redundant_closure)]
        let persistence_handler = PersistenceHandler::new(|rx| FilePersistence::new(rx));
        let ffi_handler = FFIHandler::new("python", |rx| PyCallActor::new(py_locals, rx));

        rt.block_on(async {
            local_set
                .run_until(async {
                    runtime::interpret(
                        stmts,
                        &mut glb_var_env,
                        persistence_handler,
                        ffi_handler,
                        &workflow,
                    )
                    .await
                    .unwrap_or_else(|err| {
                        eprintln!("{err:?}");
                    });
                })
                .await;
        });

        Ok(())
    })
}

#[pymodule(name = "oxiida")]
fn pyoxiida(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run, m)?)?;
    Ok(())
}
