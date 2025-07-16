import json
import pathlib

with open("built.json", "r") as fin:
    li = json.load(fin)

with open("saved.json", "r") as fin:
    poc_info = json.load(fin)

with open("db.json", "r") as fin:
    db = json.load(fin)

poc_info = dict([(i["id"], i["version_poc"]) for i in poc_info])
db = dict([(d["advisory"]["id"], d) for d in db])

for l in sorted(li):
    v = poc_info[l]
    if v == "":
        for d in (pathlib.Path("PoCs") / l).iterdir():
            if "-" in d.name:
                _, v = d.name.rsplit("-", maxsplit=1)
                break


    print("{} ({})".format(db[l]["advisory"]["package"], v))

