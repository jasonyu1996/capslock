import json
import pathlib, subprocess
import sys, os

if len(sys.argv) < 2:
    to_build_file = "success.json"
else:
    to_build_file = sys.argv[1]

if pathlib.Path(to_build_file).is_file():
    with open(to_build_file, "r") as fin:
        rustsec_ids = json.load(fin)
else:
    rustsec_ids = [to_build_file]

POC_ROOT_DIR = pathlib.Path("PoCs")

built_list = []

BUILD_TIMEOUT = 60 * 3 # timeout: 3 min

for rid in rustsec_ids:
    d = POC_ROOT_DIR / rid / "poc"
    if not d.is_dir():
        continue
    print("Building PoC for {}".format(rid), flush=True)
    # clean first
    subprocess.run(["cargo", "clean"], cwd=d)
    try:
        p = subprocess.run(["capslockbuild"], cwd=d, timeout=BUILD_TIMEOUT)
        # p = subprocess.run(["cargo"] + sys.argv[1:] + ["build", "--release", "--target", "riscv64gc-unknown-linux-gnu"], cwd=d, timeout=BUILD_TIMEOUT)
        if p.returncode == 0:
            built_list.append(rid)
    except subprocess.TimeoutExpired as _:
        print("PoC {} build timeout!".format(rid), file=sys.stderr, flush=True)

with open("built.json", "w") as fout:
   json.dump(built_list, fout, indent=2)

