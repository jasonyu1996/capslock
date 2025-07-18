use std::ffi::{OsStr, OsString};
use std::path::{Path, PathBuf};
use std::{io, iter::repeat_with};

use crate::error::IoResultExt;

fn tmpname(prefix: &OsStr, suffix: &OsStr, rand_len: usize) -> OsString {
    let capacity = prefix
        .len()
        .saturating_add(suffix.len())
        .saturating_add(rand_len);
    let mut buf = OsString::with_capacity(capacity);
    buf.push(prefix);
    let mut char_buf = [0u8; 4];
    for c in repeat_with(fastrand::alphanumeric).take(rand_len) {
        buf.push(c.encode_utf8(&mut char_buf));
    }
    buf.push(suffix);
    buf
}

pub fn create_helper<R>(
    base: &Path,
    prefix: &OsStr,
    suffix: &OsStr,
    random_len: usize,
    mut f: impl FnMut(PathBuf) -> io::Result<R>,
) -> io::Result<R> {
    let num_retries = if random_len != 0 {
        crate::NUM_RETRIES
    } else {
        1
    };

    eprintln!("Entries = {}", num_retries);
    for _ in 0..num_retries {
        eprintln!("Bef");
        let path = base.join(tmpname(prefix, suffix, random_len));
        eprintln!("Aft");
        return match f(path) {
            Err(ref e) if e.kind() == io::ErrorKind::AlreadyExists && num_retries > 1 => continue,
            // AddrInUse can happen if we're creating a UNIX domain socket and
            // the path already exists.
            Err(ref e) if e.kind() == io::ErrorKind::AddrInUse && num_retries > 1 => continue,
            res => res,
        };
    }

    Err(io::Error::new(
        io::ErrorKind::AlreadyExists,
        "too many temporary files exist",
    ))
    .with_err_path(|| base)
}
