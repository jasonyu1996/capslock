
use nanorand::*;

fn main() {
    // `x` and `y` both hold pointers to the same data in TLS (via `Rc`)
    let mut x = tls_rng();
    let mut y = tls_rng();

    // `TlsWyrand`'s `DerefMut` implementation turns this pointer into a mutable reference unconditionally
    let x_ref = &mut *x;
    let y_ref = &mut *y;

    // x_ref & y_ref now are both references to the same thing
    let _ = x_ref.rand();
    let _ = y_ref.rand();
    let _ = x_ref.rand();
}
