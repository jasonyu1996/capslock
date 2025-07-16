import json, sys, os.path

crates_set = {}

for l in sys.stdin:
    name = os.path.basename(l.strip())
    crate_name, _ = name[:name.find(".")].rsplit("-", 1)
    crates_set[crate_name] = l.strip()

with open("db.json", "w") as fout:
    json.dump(crates_set, fout)
