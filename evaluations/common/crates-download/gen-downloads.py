import json, pathlib, sys

# take file names from input

for filename in sys.stdin:
    filepath = pathlib.Path(filename.strip())
    assert(filepath.is_file())
    with open(filepath, "r") as fin:
        lines = fin.readlines()
    latest_version = {}
    for l in reversed(lines):
        try:
            latest_version = json.loads(lines[-1])
        except:
            continue
        if not latest_version["yanked"]:
            break
    if latest_version == {} or latest_version["yanked"]:
        # no available version
        continue
    print("{} {} {}".format(latest_version["name"], latest_version["vers"], latest_version["cksum"]))
