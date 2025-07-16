import json, sys

with open(sys.argv[1], "r") as fin:
    db = json.load(fin)

if len(sys.argv) > 2 and sys.argv[2] == "-x":
    # exclude
    excluded = set([l for l in sys.stdin])
    for n, p in db.items():
        if n not in excluded:
            print(p)
else:
    for l in sys.stdin:
        if l.strip() in db:
            print(db[l.strip()])
