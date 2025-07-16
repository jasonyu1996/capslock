## Experiment 2

This experiment corresponds to Section 6.2 of the paper. We
evaluate the bug finding abilities of CapsLock on existing Rust bugs collected from
[RustSec](https://rustsec.org/).
The code of the crates (along with their PoCs)
used in this experiment is located in the `PoCs` subdirectory.
In `data-prep`, we provide scripts used for preparing them.

To run this experiment without using Docker, run
```bash
sh just-run.sh [<nproc>]
```
where `<nproc>` is the number of CPU cores to use (default is 1).

