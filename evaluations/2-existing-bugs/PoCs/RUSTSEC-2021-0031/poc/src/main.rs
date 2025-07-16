
use nano_arena::{Arena, ArenaAccess, Idx};
use std::{borrow::Borrow, cell::Cell};

struct MyIdx {
    idx1: Idx,
    idx2: Idx,
    state: Cell<bool>
}

impl MyIdx {
    fn new(idx1: Idx, idx2: Idx) -> Self {
        MyIdx { idx1, idx2, state: Cell::new(false) }
    }
}

// A borrow implementation that alternatingly returns two different indexes.
impl Borrow<Idx> for MyIdx {
    fn borrow(&self) -> &Idx {
        self.state.set(!self.state.get());
        if (self.state.get()) {
            &self.idx1
        } else {
            &self.idx2
        }
    }
}

fn test_m(a_m : &mut i32, a_m2: &mut i32) {
    *a_m2 = 10;
    *a_m = 5;
    println!("{}", *a_m2);
}

fn get_refs<T>(v : &mut Vec<(T, T)>, idx : usize) -> (&mut T, &mut T) {
    let a_raw = unsafe { &mut *(v.get_mut(idx).and_then(|(_, b)| Some (b)).unwrap() as *mut T) };
    let a_raw2 = unsafe { (v.get_mut(idx).and_then(|(_, b)| Some (b)).unwrap() as *mut T).as_mut().unwrap() };
    (a_raw, a_raw2)
}

fn get_refs_i32(v : &mut Vec<(i32, i32)>, idx : usize) -> (&mut i32, &mut i32) {
    let a_raw = unsafe { &mut *(v.get_mut(idx).and_then(|(_, b)| Some (b)).unwrap() as *mut i32) };
    let a_raw2 = unsafe { (v.get_mut(idx).and_then(|(_, b)| Some (b)).unwrap() as *mut i32).as_mut().unwrap() };
    (a_raw, a_raw2)
}

fn main() {
    let mut arena = Arena::new();
    let idx1 = arena.alloc(1);
    let idx2 = arena.alloc(2);

    let custom_idx = MyIdx::new(idx1.clone(), idx2.clone());

    let (mutable_ref_one, mut split_arena) = arena.split_at(custom_idx).unwrap();
    let mutable_ref_two : &mut i32 = split_arena.get_mut(&idx1).unwrap();

    // println!("{:p} {:p}", mutable_ref_one, mutable_ref_two);
    *mutable_ref_one = 42;
    *mutable_ref_two = 30;
    println!("{}", *mutable_ref_one);

    let mut a : Vec<(i32, i32)> = vec![];
    a.push((60, 60));
    a.push((60, 60));
    a.push((60, 60));
    a.push((60, 60));
    a.push((60, 60));
    a.push((60, 60));
    a.push((60, 60));
    // let (a_m, a_m2) = get_refs(&mut a, 2);
    let (a_m, a_m2) = get_refs_i32(&mut a, 2);
    test_m(a_m, a_m2);

    // let mut a = std::sync::Arc::new(42);
    // let a_m_raw = std::sync::Arc::get_mut(&mut a).unwrap() as *mut u64;
    // let mut a2 = a.clone();
    // drop(a);
    // test_m(std::sync::Arc::get_mut(&mut a2).unwrap(), a_m_raw);

    // assert!(mutable_ref_one != mutable_ref_two);
}
