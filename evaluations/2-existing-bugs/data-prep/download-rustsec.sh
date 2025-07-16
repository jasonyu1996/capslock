set -e

RUSTSEC_REPO="https://github.com/RustSec/advisory-db"
RUSTSEC_REV="cb905e6e405834bdff1eb1e20c9b10edb5403889"
RUSTSEC_DIR=RustSec

mkdir $RUSTSEC_DIR
git -C $RUSTSEC_DIR init
git -C $RUSTSEC_DIR remote add origin $RUSTSEC_REPO
git -C $RUSTSEC_DIR fetch --depth=1 origin $RUSTSEC_REV
git -C $RUSTSEC_DIR checkout FETCH_HEAD

