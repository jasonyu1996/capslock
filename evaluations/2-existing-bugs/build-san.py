# Build PoCs with LLVM sanitisers enabled

import json
import pathlib, subprocess
import sys, os

with open("success.json", "r") as fin:
    rustsec_ids = json.load(fin)

POC_ROOT_DIR = pathlib.Path("PoCs")

built_list = []

BUILD_TIMEOUT = 60 * 3 # timeout: 3 min

san_name = sys.argv[1]

for rid in rustsec_ids:
    d = POC_ROOT_DIR / rid / "poc"
    if not d.is_dir():
        continue
    print("Building PoC for {}".format(rid), flush=True)
    subprocess.run(["cargo", "clean"], cwd=d)
    env = os.environ.copy()
    env["RUSTFLAGS"] = "-Z sanitizer={}".format(san_name)
    try:
        p = subprocess.run(["cargo", "build", "--target", "x86_64-unknown-linux-gnu"], env=env, cwd=d, timeout=BUILD_TIMEOUT)
        if p.returncode == 0:
            built_list.append(rid)
    except subprocess.TimeoutExpired as _:
        print("PoC {} build timeout!".format(rid), file=sys.stderr, flush=True)

with open("built-san-{}.json".format(san_name), "w") as fout:
    json.dump(built_list, fout, indent=2)
