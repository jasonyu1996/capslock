import subprocess, sys, pathlib, hashlib

crate_name, vers, cksum = sys.argv[1].split()

folder = pathlib.Path("data") / cksum[0:2] / cksum[2:4]
folder.mkdir(exist_ok=True,parents=True)

url = "https://static.crates.io/crates/{}/{}-{}.crate".format(crate_name, crate_name, vers)
r = subprocess.run(["curl", "-sO", url], cwd=folder)

BUF_SIZE = 65536
if r.returncode == 0:
    digest = hashlib.sha256(usedforsecurity=False)
    with open(folder / "{}-{}.crate".format(crate_name, vers), "rb") as fin:
        while True:
            data = fin.read(BUF_SIZE)
            if not data:
                break
            digest.update(data)
    if digest.hexdigest() != cksum.strip():
        print("Check failed {} {}".format(crate_name, vers), file=sys.stderr)
else:
    print("Failed {} {}".format(crate_name, vers), file=sys.stderr)
