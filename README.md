
## CapsLock Artefacts

This repository contains the artefacts for the CCS '25 paper "Securing Mixed Rust with Hardware Capabilities."

### Setup

Make sure you have Docker installed on your system, as we use Docker to set up the dependencies.

```
./build-docker # build Docker image
./build-tools # build software artefacts
```


### Usage

Build a Rust project:
```bash
./docker-build <path-to-rust-project>
```

Run a binary:
```bash
./docker-run <path-to-riscv-elf-binary>
```

### Quick Tests

You can look at the `tests` directory for some quick tests of your setup.
You can use `./docker-test` to run both tests.

- `helloworld`: Prints out "Hello, world!"
- `violation`: Triggers an error in CapsLock "Attempting to use an invalid capability for load"

### Experiments

Simply run `./docker-eval1` through `./docker-eval3` to run the respective experiments.
You can supply an optional argument to specify the number of CPU cores to use (default is 1).

Details about the experiments can be found in the `evaluations` directory.
