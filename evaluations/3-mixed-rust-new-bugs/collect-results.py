import json, pathlib

cnt_bugs = 0

for f in pathlib.Path("results").iterdir():
    with open(f, "r") as fin:
        l = json.load(fin)
    print(f"{f.name}:")
    found_bug = False
    for testcase, res in l.items():
        if len(res["capslock"]["errors"]) > 0 and len(res["miri"]["errors"]) > 0:
            err_capslock = ''.join(res['capslock']['errors'])
            err_miri = ''.join(res['miri']['errors'])
            print(f"  {testcase}:")
            print(f"    CapsLock: {err_capslock}")
            print(f"    Miri: {err_miri}")

            if "[CAPSLOCK]" in err_capslock and "unsupported operation" in err_miri:
                found_bug = True

    if found_bug:
        cnt_bugs += 1

print(f"SUMMARY: {cnt_bugs} bugs found")
