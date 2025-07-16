use dashmap::DashMap;

fn main() {
    let x = DashMap::new();

    x.insert(1, 1);

    let one: &i32 = {
        let borrow = x.get(&1).unwrap();
        let val = borrow.value();
        std::mem::drop(borrow); // !!!
        val
    };

    println!("{}", one); // Prints `1`

    for i in 0..100 {
        x.insert(i, i + 1);
    }

    println!("{}", one); // Prints `2`!
}
