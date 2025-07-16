import json, urllib.request, sys

if len(sys.argv) < 2:
    print("Provide the number of crates to list!", file=sys.stderr)
    exit(1)

N = int(sys.argv[1])
counts = 0
page = 1
while counts < N:
    with urllib.request.urlopen("https://crates.io/api/v1/crates?sort=downloads&page={}".format(page)) as f:
        data = json.load(f)
    for c in data["crates"]:
        print(c["id"])
        counts += 1
        if counts == N:
            break
    page += 1
