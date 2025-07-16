
## CapsLock Artefacts

### Setup

Make sure you have Docker installed on your system.

You can build the Docker image from the provided `Dockerfile`:
```
./build-docker
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

NOTE: The Docker container will run with UID 1000. Please make sure that
the files are accessible to it. You can achieve this by running the following
in the host environment:
```
chown -R 1000:1000 evaluations src tests
```

You may also need to open up permissions
```
chmod -R 777 evaluations src tests
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
