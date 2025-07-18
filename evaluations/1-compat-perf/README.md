## Experiment 1

This directory corresponds to Sections 6.1 and 6.4 of the paper, where we run
on CapsLock the test cases bundled with the top 100 popular crates from crates.io.
We report both the results of the runs and the performance of CapsLock in terms of
the time taken to run the tests.
In `data-prep`, we provide scripts used for collecting the list of the most popular
crates on crates.io.

### Estimated Run-time

This experiment may take up to ~10 hours even when specified to run on
multiple CPU cores, as some test cases take long to run and are not
parallelized.

### Expected Results

The standard output should include a summary of the experiment results,
which are arranged in a table and match Table 3 in the paper. In particular,
more than 99% of the test cases should pass.
The performance results should match Section 6.4 in the paper.
"Performance Average" should be lower than 50% and
the generated `performance-hist.pdf` should roughly match
Figure 7.

Detailed per-test-case results in JSON format are located in the `results` directory.
