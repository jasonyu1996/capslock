## Experiment 3

This directory corresponds to Section 6.3 of the paper, where we
evaluate the bug finding abilities of CapsLock in mixed Rust code.
Due to the size of crates.io, here we include
code only of the crates newly found to contain bugs.

### Estimated Run-time

This experiment takes an hour or less to finish.

### Expected Results

The standard output should show at least one entry for each of the 8 crates,
where Miri indicates "unsupported operation" and CapsLock indicates errors detected.
Note that for three of the cases, the bug is detected through test cases
bundled with a different crate than the crate that contains the bug:
`mozjpeg` through `jpegli`, `sxd-document` through `cargo-wix`, and
`ring` through `quinn`.

Detailed results per test case are produced in JSON format in the `results` directory.

