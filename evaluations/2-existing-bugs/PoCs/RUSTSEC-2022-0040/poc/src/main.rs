use owning_ref::OwningRef;
use std::cell::Cell;

fn helper(owning_ref: OwningRef<Box<Cell<u8>>, Cell<u8>>) -> u8 {
    owning_ref.as_owner().set(10);
    owning_ref.set(20);
    owning_ref.as_owner().get() // should return 20
}

fn main() {
    let val: Box<Cell<u8>> = Box::new(Cell::new(25));
    let owning_ref = OwningRef::new(val);
    let res = helper(owning_ref);
    assert_eq!(res, 20); // assertion fails!
}

