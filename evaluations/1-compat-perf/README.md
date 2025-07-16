## Experiment 1

This directory corresponds to Sections 6.1 and 6.4 of the paper, where we run
on CapsLock the test cases bundled with the top 100 popular crates from crates.io.
We report both the results of the runs and the performance of CapsLock in terms of
the time taken to run the tests.
In `data-prep`, we provide scripts used for collecting the list of the most popular
crates on crates.io.

If you want to run this experiment without using Docker, run
```bash
sh just-run.sh [<nproc>]
```
where `<nproc>` is the number of CPU cores to use (default is 1).
