
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

You can also attach GDB, which can help locate the source of a violation:
```bash
./docker-gdb <path-to-riscv-elf-binary>
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

### Understanding the Output

When CapsLock detects a violation during execution, it prints out an error message to stderr,
in one of the following forms:
* **Attempting to use invalid capability for store (address = {ADDR}, size = {SIZE}, node = {NODE_ADDR}) @ pc = {PC}**:
  The program attempts to use an invalid capability for storing data. This could imply either a use-after-free or
  a violation of borrowing/AXM principles.
* **Attempting to use an invalid capability for load (address = {ADDR}, size = {SIZE}, node = {NODE_ADDR}) @ pc = {PC}**:
  The program attempts to use an invalid capability for loading data. This could imply either a use-after-free or
  a violation of borrowing/AXM principles.
* **Attempting to borrow from an invalid capability (node = {NODE_ADDR}, {NODE_ID}) addr = {ADDR}, size = {SIZE} @ pc = {PC}**:
  The program attempts to borrow from an invalid capability. This could imply a violation of ownership/borrowing/AXM principles.
* **Attempting to drop an invalid capability! {ADDR} {NODE_ADDR} in {PID} @ {PC}, previously invalidated at {PC_PREV}**:
  The program attempts to free an object using an invalid capability. This could imply a double-free and a violation of the
  ownership principle.
* **Capability access OOB {ADDR} size = {SIZE} @ pc = {PC}**:
  The program attempts to access memory outside the bounds of a capability. This could imply a violation of spatial memory
  safety.

The details provided in the error message can help understand the cause and the location of the violation:
* **ADDR** and **SIZE** are the base address and the size of the memory access, respectively.
* **PC** is the program counter address at the point of detection.
* **PC_PREV** is the program counter address when the capability was previously invalidated.
* [Debug] **NODE_ADDR** and **NODE_ID** are the address and identifier of the location where the capability
  metadata is maintained, used mostly for debugging CapsLock itself.
* [Debug] **PID** is the process ID of the QEMU process that reports the violation, used for debugging CapsLock itself.

### License

Please see [LICENSE](/LICENSE).
