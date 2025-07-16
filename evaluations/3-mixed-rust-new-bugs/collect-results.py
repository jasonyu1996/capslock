import json, pathlib

for f in pathlib.Path("results").iterdir():
    with open(f, "r") as fin:
        l = json.load(fin)
    print(f"{f.name}:")
    for testcase, res in l.items():
        if len(res["capslock"]["errors"]) > 0 and len(res["miri"]["errors"]) > 0:
            print(f"  {testcase}:")
            print(f"    CapsLock: {''.join(res['capslock']['errors'])}")
            print(f"    Miri: {''.join(res['miri']['errors'])}")

