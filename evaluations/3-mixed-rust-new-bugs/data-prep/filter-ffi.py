import json, sys, subprocess

GREP_CMD = ["timeout", "1", "find", ".", "-type", "f", "-name", "*.rs",
        "!", "-path", "./target/*",
        "-exec",
        "grep", "-wqE", "ffi|bindgen|#\\[link", "{}", "+"]

with open("db.json", "r") as fin:
    db = json.load(fin)

with_ffi_list = []
for i, (n, p) in enumerate(db.items()):
    r = subprocess.run(GREP_CMD, cwd=p)
    if r.returncode == 0:
        # found
        with_ffi_list.append(n)
    if i % 10 == 0:
        print("\r{}".format(i), end="", flush=True)


with open("ffi.json", "w") as fout:
    for l in with_ffi_list:
        print(l, file=fout)
    # json.dump(with_ffi_list, fout, indent=2)
