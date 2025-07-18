## Experiment 2

This experiment corresponds to Section 6.2 of the paper. We
evaluate the bug finding abilities of CapsLock on existing Rust bugs collected from
[RustSec](https://rustsec.org/).
The code of the crates (along with their PoCs)
used in this experiment is located in the `PoCs` subdirectory.
In `data-prep`, we provide scripts used for preparing them.

### Estimated Run-time

This experiment is not parallelized (thus ignoring the
specified CPU core number). It is expected to take less
than 1 hour to finish.

### Expected Results

The standard output includes a summary of the
errors reported by CapsLock and baseline tools. The results should
match Table 4 in the paper. In particular, CapsLock should report
errors for all 15 test cases.

The full output produced by CapsLock for each test case is logged
under the `run-logs` directory.
