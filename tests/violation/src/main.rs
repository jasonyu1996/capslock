use std::arch::asm;

fn main() {
    let mut d = Box::new(42);
    let p_raw = &mut *d as *mut i32;
    unsafe {
        asm!("sw x0, 0({})", in(reg) (&mut *d));
    }
    println!("{}", unsafe { *p_raw });
}
