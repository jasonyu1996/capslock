use algorithmica::sort::merge_sort::sort;

fn main() {
    let mut arr = vec![
        String::from("Hello"),
        String::from("World"),
        String::from("Rust"),
    ];

    // Calling `merge_sort::sort` on an array of `T: Drop` triggers double drop
    algorithmica::sort::merge_sort::sort(&mut arr);
    dbg!(arr);
}
