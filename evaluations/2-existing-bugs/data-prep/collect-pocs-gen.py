import json, pathlib, shutil
import sys

with open("built-san.json", "r") as fin:
    built_pocs = json.load(fin)


TARGET_DIR = pathlib.Path(sys.argv[1])
POCS_ROOT_DIR = pathlib.Path("./PoCs")


for poc in built_pocs:
    print("Copying {}".format(poc))
    poc_file = POCS_ROOT_DIR / poc / "poc" / "target" / "x86_64-unknown-linux-gnu" / "debug" / "poc"
    assert(poc_file.is_file())
    dest_file = TARGET_DIR / poc
    shutil.copy(poc_file, dest_file)

