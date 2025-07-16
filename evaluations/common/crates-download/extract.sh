(cd data; find . -type f -name '*.crate') | parallel -j16 --bar 'mkdir -p data-extracted/$(dirname {}) && tar -C data-extracted/$(dirname {}) -xzf $(pwd)/data/{}'
