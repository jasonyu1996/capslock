import json, sys, subprocess
import pathlib

if len(sys.argv) < 2 or sys.argv[1].endswith(".json"):
    fname = "built.json" if len(sys.argv) < 2 else sys.argv[1]
    with open(fname, "r") as fin:
        poc_list = sorted(json.load(fin))
else:
    poc_list = sys.argv[1:]

with open("filtered.json", "r") as fin:
    db = json.load(fin)

db = dict([(d["advisory"]["id"], d) for d in db])

file_list = [("./PoCs/{}/poc/src/main.rs".format(poc), "./.edit/{}.rs".format(poc), db[poc]) for poc in poc_list]

pathlib.Path("./.edit").mkdir(exist_ok=True)

for src_file, target_file, entry in file_list:
    header_lines = [
        "ID: {}".format(entry["advisory"]["id"]),
        "RustSec: https://rustsec.org/advisories/{}.html".format(entry["advisory"]["id"]),
        "Package: {}".format(entry["advisory"]["package"]),
        "Keywords: {}".format(", ".join(entry["advisory"].get("keywords", []))),
        "URLs: {}".format(" ".join(entry["likely_poc"])),
        "Patched: {}".format(",".join(entry["versions"].get("patched", []))),
        "Unaffected: {}".format(",".join(entry["versions"].get("unaffected", []))),
    ]
    header_lines = ["// {}\n".format(s) for s in header_lines] + ["//// END OF HEADERS ////\n"]
    with open(target_file, "w") as fout:
        fout.write("".join(header_lines))
        with open(src_file, "r") as fin:
            fout.write(fin.read())

edit_file_list = list(map(lambda x: x[1], file_list))
edit_file_mtime_orig = list(map(lambda x: pathlib.Path(x).stat().st_mtime_ns, edit_file_list))

p = subprocess.run(["vim"] + edit_file_list)

if p != 0:
    # successful edit, write back the changes
    for (src_file, target_file, entry), mtime_orig in zip(file_list, edit_file_mtime_orig):
        if pathlib.Path(target_file).stat().st_mtime_ns != mtime_orig:
            with open(target_file, "r") as fin:
                for l in fin:
                    if "END OF HEADERS" in l:
                        break
                with open(src_file, "w") as fout:
                    fout.write(fin.read())
            print("PoC {} updated".format(entry["advisory"]["id"]))

