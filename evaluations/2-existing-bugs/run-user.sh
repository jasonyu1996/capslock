# Run with QEMU user mode emulation

rustsec_id=$1

# qemu-capslock
timeout 20 \
    capslockrun PoCs/$rustsec_id/poc/target/riscv64gc-unknown-linux-gnu/debug/poc
