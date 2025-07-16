import subprocess, json, pathlib, shutil
import sys

with open("built.json", "r") as fin:
    built_pocs = json.load(fin)


BUILDROOT_DIR = pathlib.Path("../../captainer-buildroot")
BUILDROOT_OVERLAY_DIR = BUILDROOT_DIR / "overlay"
POCS_ROOT_DIR = pathlib.Path("./PoCs")

if len(sys.argv) < 2:
    profile = "debug"
else:
    profile = sys.argv[1]


for poc in built_pocs:
    print("Copying {}".format(poc))
    poc_file = POCS_ROOT_DIR / poc / "poc" / "target" / "riscv64gc-unknown-linux-gnu" / profile / "poc"
    assert(poc_file.is_file())
    dest_file = BUILDROOT_OVERLAY_DIR / poc
    shutil.copy(poc_file, dest_file)


print("Building image")
subprocess.run(["make", "build", "-j8"], cwd=BUILDROOT_DIR)

