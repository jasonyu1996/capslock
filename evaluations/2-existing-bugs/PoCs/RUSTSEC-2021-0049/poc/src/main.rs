use through::through;

fn main() {
    let mut hello = String::from("Hello");
    let object = through(&mut hello, |mut s| {
        s.push_str(" World!");
        panic!("Unexpected panic");
        s
    });
    dbg!(object);
}
