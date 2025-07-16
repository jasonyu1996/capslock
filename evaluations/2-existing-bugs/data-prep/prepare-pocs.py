# This grabs the affected crates and prepares the PoCs

import json
import pathlib
import urllib.request
import subprocess
import sys, re

with open("saved.json", "r") as fin:
    pocs = json.load(fin)

with open("filtered.json", "r") as fin:
    db = json.load(fin)

try:
    with open("success.json", "r") as fin:
        success = json.load(fin)
except:
    success = []

skip_set = set(success)

# combine
db = dict((d["advisory"]["id"], d) for d in db)
for p in pocs:
    db[p["id"]]["poc"] = p["poc"]
    db[p["id"]]["version_poc"] = p["version_poc"]

ROOT_POC_DIR = pathlib.Path("./PoCs")


def update_prompt(s, r=False):
    if r:
        print("\r{}".format(s), end="", flush=True)
    else:
        print(s, end="", flush=True)

def is_hash(v):
    return len(v) > 2 and '.' not in v

def query_crates_io(s):
    return json.load(urllib.request.urlopen("https://crates.io/api/v1/{}".format(s)))

VERSION_STRING = re.compile("\d+\.\d+\.\d+")

def download_crate(dest, package_name, version):
    # check if the version is a hash
    try:
        info = query_crates_io("crates/{}".format(package_name))
    except:
        return None
    if is_hash(version):
        # for hash version number, get it from github, but where?
        try:
            repo_url = info["crate"]["repository"]
        except:
            return None
        if not repo_url:
            return None
        git_dest = dest / package_name
        p = subprocess.run(["git", "clone", repo_url, str(git_dest)])
        if p.returncode != 0:
            # failed to clone the repo
            return None
        p = subprocess.run(["git", "-C", str(git_dest), "checkout", version])
        return None if p.returncode != 0 else git_dest
    else:
        try:
            v = version or info["crate"]["max_version"]
            # check for versions
            vs = info["versions"]
        except:
            return None
        if not v or not vs:
            return None
        rv = None
        for vv in vs:
            dl_path = vv["dl_path"]
            # get the version string
            m = re.search(VERSION_STRING, dl_path)
            if not m:
                continue
            ms = m.group(0)
            if ms.startswith(v):
                rv = ms
                break
        if not rv:
            return None
        target_file = dest / "{}.tar.gz".format(package_name)
        p = subprocess.run(["wget", "-O", str(target_file), "https://crates.io/api/v1/crates/{}/{}/download".format(package_name, rv)])
        if p.returncode != 0:
            return None
        p = subprocess.run(["tar", "xzf", str(target_file.absolute())], cwd=target_file.parent)
        if p.returncode != 0:
            return None
        return dest / "{}-{}".format(package_name, rv)


CONFIG_TOML_CONTENT = """
[target.riscv64gc-unknown-linux-gnu]
rustflags = ["--capstone=*", "-C", "target-feature=+crt-static"]
linker = "riscv64-linux-gnu-gcc"
"""

def prepare_poc_crate(dest, poc, crate_name, crate_dir):
    p = subprocess.run(["cargo", "new", str(dest), "--bin"])
    if p.returncode != 0:
        return False
    try:
        with open(dest / "src" / "main.rs", "w") as fout:
            fout.write(poc)
        with open(dest / "Cargo.toml", "a") as fout:
            fout.write("\n{} = {{ path = \"{}\" }}\n".format(crate_name, "../{}".format(crate_dir.name)))
        cargo_dir = dest / ".cargo"
        cargo_dir.mkdir(exist_ok=True)
        with open(cargo_dir / "config.toml", "w") as fout:
            fout.write(CONFIG_TOML_CONTENT)
    except:
        return False
    return True

def test():
    print(json.dumps(query_crates_io("crates/nanorand"), indent=2))

for idx, entry in enumerate(db.values()):
    if not entry["poc"]:
        continue
    rustsec_id = entry["advisory"]["id"]
    package_name = entry["advisory"]["package"]
    version = entry["version_poc"]
    poc = entry["poc"]

    if rustsec_id in skip_set:
        continue

    update_prompt("Preparing {} ({}/{}) ...".format(rustsec_id, idx + 1, len(db)), r=True)
    poc_dir = ROOT_POC_DIR / rustsec_id
    poc_dir.mkdir(exist_ok=True)

    crate_dir = download_crate(poc_dir, package_name, version.strip())
    if not crate_dir:
        print("Failed to fetch crate {}!".format(package_name), file=sys.stderr)
        continue
    if not prepare_poc_crate(poc_dir / "poc", poc, package_name, crate_dir):
        print("Failed to write PoC to files", file=sys.stderr)
        continue

    # prepare Cargo.toml
    success.append(rustsec_id)

with open("success.json", "w") as fout:
    json.dump(success, fout, indent=2)
