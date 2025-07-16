sed "s+LLVM_LOCATION+$(pwd)/../llvm+" /scripts/build/rust-config.toml > config.toml
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/../llvm/installation/lib ./x.py build compiler library src/tools/cargo --stage 2 --target=riscv64gc-unknown-linux-gnu --jobs 8
rustup toolchain link capslock build/host/stage2 || true

