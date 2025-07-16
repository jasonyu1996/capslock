import subprocess, json, pathlib, resource
import sys

with open("built-san-{}.json".format(sys.argv[1]), "r") as fin:
    to_run_list = sorted(json.load(fin))

TIMEOUT = 60 * 3

def limit_mem():
    resource.setrlimit(resource.RLIMIT_RSS, (1024 * 1024 * 1024 * 8, resource.RLIM_INFINITY))

for rustsec_id in to_run_list:
    executable = pathlib.Path("PoCs") / rustsec_id / "poc" \
        / "target" / "x86_64-unknown-linux-gnu" / "debug" / "poc"
    print("#### Running {}".format(rustsec_id), flush=True)
    try:
        p = subprocess.run([executable], timeout=TIMEOUT, preexec_fn=limit_mem)
        success = p == 0
    except subprocess.TimeoutExpired:
        print("#### Timeout!")
        success = False

    if success:
        print("#### {} success".format(rustsec_id), flush=True)
    else:
        print("#### {} failure".format(rustsec_id), flush=True)

