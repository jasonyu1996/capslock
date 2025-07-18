
## CapsLock Artefacts

This repository contains the artefacts for the CCS '25 paper "[Securing Mixed Rust with Hardware Capabilities](https://arxiv.org/abs/2507.03344)."

### Setup

We use Docker to set up the dependencies.
Make sure you have Docker installed on your system, and check
```bash
# you may need to add your user to the "docker" group
docker run hello-world # make sure you can run Docker containers
id -u # should be >= 1000
```

Now run the following
```bash
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

Details about the experiments, including their estimated run-times and expected results
can be found in the `evaluations` directory.

### License

Please see [LICENSE](/LICENSE).
