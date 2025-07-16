

use qcell::{TCell, TCellOwner};

type T1 = fn(&());
type T2 = fn(&'static ());

// T1 subtype of T2, both 'static

// TCellOwner covariant
fn _demo(x: TCellOwner<T1>) -> TCellOwner<T2> {
    x
}

// and that's obviously bad

fn main() {
    let first_owner = TCellOwner::<T2>::new();
    let mut second_owner = TCellOwner::<T1>::new() as TCellOwner<T2>;

    let mut x = TCell::<T2, _>::new(vec!["Hello World!".to_owned()]);
    let reference = &first_owner.ro(&x)[0];
    second_owner.rw(&x).clear();

    println!("{}", reference); // ��&d��i
                               // (or similar output)
}
