FROM ubuntu:22.04 AS base

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID user && useradd -u $UID -g $GID -m user
ENV DEBIAN_FRONTEND=noninteractive

# common build and runtime dependencies

FROM base AS depends

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update && apt-get install -y curl ninja-build make gcc g++
# RUN rustup install 1.85.1 && rustup default 1.85.1
RUN apt-get install -y gcc-riscv64-linux-gnu g++-riscv64-linux-gnu
RUN apt-get install -y git python3 python3-venv
RUN apt-get build-dep -y qemu
RUN apt-get build-dep -y llvm
RUN apt-get install -y cmake
RUN apt-get install -y parallel
RUN apt-get install -y python3-matplotlib python3-numpy

RUN mkhomedir_helper user

USER user

ADD --chown=user:user build /scripts/build
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh /dev/stdin --default-toolchain none -y
ENV PATH="/home/user/.cargo/bin:${PATH}"
ARG RUST_TOOLCHAIN=nightly-2024-05-26
RUN rustup install $RUST_TOOLCHAIN && rustup default $RUST_TOOLCHAIN
RUN rustup +$RUST_TOOLCHAIN component add miri rust-src
RUN ln -s /home/user/.rustup/toolchains/$RUST_TOOLCHAIN-x86_64-unknown-linux-gnu \
          /home/user/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu

# RUN rustup toolchain link capslock /capslock-tools/rust/build/host/stage2

ADD --chown=user:user bin /capslock/bin


ENV PATH="/capslock/bin:/capslock-tools/qemu/installation/bin:${PATH}" \
    LD_LIBRARY_PATH="/capslock-tools/llvm/installation/lib"
    # RUSTFLAGS="-C target-feature=+crt-static" \
    # CARGO_TARGET_RISCV64GC_UNKNOWN_LINUX_GNU_LINKER="riscv64-linux-gnu-gcc"

ENTRYPOINT ["/capslock/bin/capslockentry"]
