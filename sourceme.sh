CURDIR=$(pwd)/setup

export PATH="${CURDIR}/bin:${CURDIR}/qemu/installation/bin:${PATH}"
export LD_LIBRARY_PATH="${CURDIR}/llvm/installation/lib:${LD_LIBRARY_PATH}"
export RUSTFLAGS="-Z unstable-options -C target-feature=+crt-static"
export CARGO_TARGET_RISCV64GC_UNKNOWN_LINUX_GNU_LINKER="riscv64-linux-gnu-gcc"
