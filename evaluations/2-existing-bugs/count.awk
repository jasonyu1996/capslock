BEGIN {
    cnt = 0;
    first = 0;
}

/Running RUSTSEC/ {
    first = 1;
}

/AddressSanitizer|ThreadSanitizer|Undefined Behavior/ {
    if (first) {
        ++ cnt;
    }
    first = 0;
}

END {
    print(cnt);
}
