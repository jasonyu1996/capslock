import subprocess, pathlib, json
import resource

with open("built-san-address.json", "r") as fin:
    to_run_list = sorted(json.load(fin))

TIMEOUT = 60 * 3

def limit_mem():
    resource.setrlimit(resource.RLIMIT_RSS, (1024 * 1024 * 1024 * 8, resource.RLIM_INFINITY))

for rustsec_id in to_run_list:
    root_dir = pathlib.Path("PoCs") / rustsec_id / "poc"
    print("#### Running {}".format(rustsec_id), flush=True)
    try:
        p = subprocess.run(["cargo", "miri", "run"], cwd=root_dir, timeout=TIMEOUT, preexec_fn=limit_mem)
        success = p == 0
    except subprocess.TimeoutExpired:
        print("#### Timeout!")
        success = False

    if success:
        print("#### {} success".format(rustsec_id), flush=True)
    else:
        print("#### {} failure".format(rustsec_id), flush=True)

