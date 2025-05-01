# oxiida

[![Documentation](https://img.shields.io/badge/docs-online-green)](https://oxiida.github.io/book/)

`oxiida` is a workflow interpreter for building and controlling processes running on remote resources.
It is opinioned on focusing at running scientific workflows in a high-throughput manner.

- `oxiida` supports construct and run tasks/jobs with different timespan from seconds to months. 
- `oxiida` supports run tasks/jobs on local machine, cloud or HPC.
- `oxiida` has native support for Workflow Definition Language (WDL).
- `oxiida` as a language can embed into Python, Julia and Lua to powerup and standard your current workflow setup.

## Installation

### Pre-compiled binaries

Download the Oxiida binary from [SourceForge](https://sourceforge.net/projects/oxiida/files/) and place it somewhere in your system’s `PATH`.

### From a programming language 

If you intend to call Oxiida from Python, <!--Julia, or Lua-->, install the corresponding `oxiida` library:

| Language | Package manager command |
| -------- | ----------------------- |
| Python   | `pip install oxiida`    |
<!-- | Julia (not yet avail)  | `import Pkg; Pkg.add("Oxiida")` | -->
<!-- | Lua (not yet avail)    | `luarocks install oxiida` | -->

## Disclaimer

The name comes from `oxiida` is the oxidized (it is rusty :crab:) [AiiDA](https://aiida.net), the workflow engine my team are developing.
It is not just another rewrite into rust project, instead I try to redesign it into a standard DSL.

## License

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the 
Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.

