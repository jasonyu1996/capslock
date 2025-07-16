set -e

IDX_REPO="https://github.com/rust-lang/crates.io-index.git"
IDX_REV="930e12e5da8abc2b518ee979c313165a1edced7e" # revision used in experiments
IDX_DIR="crates.io-index"

# download crates.io index
if [ ! -d crates-io ]; then
    mkdir $IDX_DIR
    git -C $IDX_DIR init
    git -C $IDX_DIR remote add origin $IDX_REPO
    git -C $IDX_DIR fetch --depth=1 origin $IDX_REV
    git -C $IDX_DIR checkout FETCH_HEAD
fi

find crates.io-index/ -type f -not -path '*.json' -not -path '*/.github/*' -not -path '*/.git/*' | python3 gen-downloads.py | parallel -j16 --bar python3 download-single.py
