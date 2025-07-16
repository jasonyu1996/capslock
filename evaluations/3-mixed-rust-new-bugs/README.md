## Experiment 3

This directory corresponds to Section 6.3 of the paper, where we
evaluate the bug finding abilities of CapsLock in mixed Rust code.
Due to the size of crates.io, here we include
code only of the crates newly found to contain bugs.

To run the experiment without using Docker, run
```bash
sh just-run.sh [<nproc>]
```
where `<nproc>` is the number of CPU cores to use (default is 1).
