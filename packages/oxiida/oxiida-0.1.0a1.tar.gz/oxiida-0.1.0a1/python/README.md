# oxiida

`oxiida` is a workflow interpreter for building and controlling processes running on remote resources.
It is opinioned on focusing at running scientific workflows in a high-throughput manner.

- `oxiida` supports construct and run tasks/jobs with different timespan from seconds to months. 
- `oxiida` supports run tasks/jobs on local machine, cloud or HPC.
- `oxiida` has native support for Workflow Definition Language (WDL).
- `oxiida` as a language can embed into Python, Julia and Lua to powerup and standard your current workflow setup.

## Construct workflow in Python

Similar as using the arithmetic, now I need to run a function (let's say I want to do high school match with `math.sin(x)`, and a customize function to compute some nonsense stuff).
And this function is defineded or imported in python.
I can run it from Oxiida and also surpass the GIL!

```python
import oxiida
import math
from time import sleep, time

def super_complex_operation(x: float, y: float, z: float) -> float:
    intermediate1 = math.sin(x) * math.log1p(abs(y))
    intermediate2 = math.exp(-z) + x ** 2
    # Sleep 2 sec to demostrat two of them can run concurrently without GIL limitation
    sleep(2);
    result = (intermediate1 + intermediate2) / (1 + abs(z - y))
    print("time:", time.strftime("%Y-%m-%d %H:%M:%S"))
    return result

# language = oxiida
workflow = """
require super_complex_operation;
require time, sleep;

para {
    print "--anchor--";
    seq {
        print(super_complex_operation(10, 3, 6));
    }

    seq {
        print(super_complex_operation(5.4, 3, 7));
    }
}
"""

if __name__ == '__main__':
    oxiida.run(workflow)
```

The powerfulness of running python function within Oxiida is you are not limited by the python GIL anymore.
Using `para` block syntax allow to call both functions to run concurrently in separate threadings.


## Disclaimer

The name comes from `oxiida` is the oxidized (it is rusty :crab:) [AiiDA](https://aiida.net), the workflow engine my team are developing.
It is not just another rewrite into rust project, instead I try to redesign it into a standard DSL.

## License

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the 
Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.

