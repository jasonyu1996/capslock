# Script to extract a list of test cases for a crate

import sys, subprocess, pathlib, os
import json

def get_package_name(p):
    s = p.strip().rsplit("/", 1)[1]; d = s.split(".", 1)[0].rfind("-")
    return s[:d] + "@" + s[d+1:]

path = sys.argv[1]
package_name = get_package_name(path)

TIMEOUT_BUILD=300

SETUPS = [
    ("capslock", ["+capslock"], "riscv64gc-unknown-linux-gnu", {}),
    ("miri", ["+nightly"], "x86_64-unknown-linux-gnu", {"RUSTFLAGS": "--cfg miri"}),
    ("x86_64", ["+nightly"], "x86_64-unknown-linux-gnu", {})
]

res = {}

for setup_name, extra_switch, target, extra_env in SETUPS:
    p = subprocess.run(
        ["timeout", str(TIMEOUT_BUILD)]
        + ["cargo"]
        + extra_switch
        + [
            "test", "-j4",
            "--target={}".format(target),
            "-p", package_name,
            "--tests",
            "--",
            "-Z", "unstable-options",
            "--list",
            "--format", "json"
        ],
        # timeout=TIMEOUT_BUILD,
        capture_output=True,
        env=os.environ | extra_env,
        cwd=path,
        text=True
    )
    li = {}
    if p.returncode == 0:
        # build a map from source file to integration test name
        # print(p.stderr)
        integration_map = {}
        for l in p.stderr.splitlines():
            s = l.strip().split()
            try:
                idx = s.index("Running")
                source_name = s[idx + 1]
                target_name = s[idx + 2][1:-1]
                target_name = pathlib.Path(target_name).name
                target_name = target_name.rsplit("-")[0]
                integration_map[source_name] = target_name
            except:
                continue

        for l in p.stdout.splitlines():
            try:
                test_case = json.loads(l.strip())
            except:
                continue
            if test_case["type"] == "test" and test_case["event"] == "discovered":
                source_name = test_case["source_path"]
                integration_name = integration_map.get(source_name, "") # empty string indicates unit tests
                test_case_path_name = "{}>{}".format(integration_name, test_case["name"])
                if test_case_path_name in li:
                    print("{}: Test case name already seen: {}".format(path, test_case_path_name), file=sys.stderr)
                # assert(test_case_path_name not in li)
                li[test_case_path_name] = test_case["ignore"]
    else:
        print(p.stderr)
    res[setup_name] = {
        "success": p.returncode == 0,
        "tests": li
    }
    subprocess.run(["cargo"] + extra_switch + ["clean"], cwd=path, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        env=os.environ | extra_env)

print(json.dumps(res, indent=2))
