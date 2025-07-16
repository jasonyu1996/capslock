# Run tests one by one

import sys, subprocess, pathlib, os, signal
import json

def get_package_name(p):
    s = p.strip().rsplit("/", 1)[1]; d = s.split(".", 1)[0].rfind("-")
    return s[:d] + "@" + s[d+1:]

def get_test_list(testcases):
    miri_tests = testcases["miri"]["tests"]
    capslock_tests = testcases["capslock"]["tests"]
    x86_tests = testcases["x86_64"]["tests"]

    test_list = []
    for test_name, miri_ignore in miri_tests.items():
        capslock_ignore = capslock_tests.get(test_name, True)
        x86_ignore = x86_tests.get(test_name, True)

        if (not capslock_ignore) and ((not miri_ignore) or (not x86_ignore)):
            test_list.append((test_name, miri_ignore))
    return test_list

cur_dir = os.getcwd()
path = sys.argv[1]
package_name = get_package_name(path)

test_case_file = pathlib.Path(path) / "testcases.json"
test_results_file = (pathlib.Path(path) / "run-results.json") if len(sys.argv) < 3 else pathlib.Path(sys.argv[2])

FFI_ONLY=("FFI_ONLY" in os.environ.keys())
RERUN_MIRI=("RERUN_MIRI" in os.environ.keys())
BUILD_TIMEOUT=180
TIMEOUT=60
EXTRA_TIMEOUT=10


if test_results_file.is_file() and not RERUN_MIRI:
    try:
        with open(test_results_file, "r") as fin:
            test_results = json.load(fin)
    except:
        test_results = {}
else:
    test_results = {}

if test_case_file.is_file():
    with open(test_case_file, "r") as fin:
        try:
            testcases = json.load(fin)
            test_list = get_test_list(testcases)
        except:
            test_list = []
    os.chdir(path)
    for full_test_name, miri_ignore in test_list:
        # print("#### Testing {}, miri ignore = {}".format(test_name, miri_ignore))
        # get the test selection arguments
        target_name, test_name = full_test_name.split(">")
        if target_name == "":
            select_args = ["--lib"] # unit test
        else:
            select_args = ["--test", target_name] # integration test
        # Run on MIRI
        if not RERUN_MIRI and (full_test_name in test_results):
            miri_result = test_results[full_test_name]["miri"]
        elif miri_ignore:
            miri_result = {
                "result": "ignored",
                "summary": "",
                "errors": [],
                "exit_code": 0
            }
        else:
            subprocess.run(
                [
                    "timeout", "-k", str(EXTRA_TIMEOUT), str(BUILD_TIMEOUT),
                    "cargo", "miri", "test",
                ]
                + select_args
                + ["--no-run"],
                env=os.environ | {"MIRIFLAGS": "-Zmiri-disable-isolation"},
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            p = subprocess.run(
                [
                    "timeout", "-k", str(EXTRA_TIMEOUT), str(TIMEOUT),
                    "cargo", "miri", "test",
                ]
                + select_args
                + [
                    "--",
                    "--test-threads", "1",
                    "--exact", test_name,
                    "-Z", "unstable-options",
                    "--format", "json"
                ],
                # cwd=path,
                capture_output=True,
                env=os.environ | {"MIRIFLAGS": "-Zmiri-disable-isolation"},
                text=True,
                start_new_session=True
            )
            if p.returncode == 124:
                # timed out
                result = "timeout"
                summary = {}
                error_msgs = []
                exit_code = 0
                summary = {}
            else:
                summary = {}
                for l in p.stdout.splitlines():
                    try:
                        res = json.loads(l.strip())
                        if "passed" in res:
                            # ok we have found it
                            summary = res
                            break
                    except:
                        pass
                # search in the error stream for violations
                error_msgs = []
                for l in p.stderr.splitlines():
                    if "unsupported operation" in l or "Undefined Behavior" in l:
                        error_msgs.append(l)
                # if p.returncode != 0:
                #     error_msgs = p.stderr.splitlines()
                result = "finished"
                # print(p.args, file=sys.stderr)
                # print(p.stderr, file=sys.stderr)
                exit_code = p.returncode
            miri_result = {
                "result": result,
                "summary": summary,
                "errors": error_msgs,
                "exit_code": exit_code
            }

        if FFI_ONLY and len(miri_result["errors"]) == 0: # no unsupported operations
            capslock_result = {
                "result": "skipped",
                "summary": {},
                "errors": [],
                "exit_code": 0
            }
        else:
            # we only run CapsLock when MIRI encounters unsupported operations
            # Run on Capslock
            # build first
            try:
                subprocess.run(
                    [
                        "timeout", "-k", str(EXTRA_TIMEOUT), str(BUILD_TIMEOUT),
                        "cargo", "+capslock", "test", "--target=riscv64gc-unknown-linux-gnu",
                        "-p", package_name,
                    ]
                    + select_args
                    + ["--no-run"], # just build
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=BUILD_TIMEOUT
                )
            except:
                pass
            try:
                # p = subprocess.run(["true"], capture_output=True, text=True, start_new_session=True)
                p = subprocess.run(
                    [
                        "timeout", "-k", str(EXTRA_TIMEOUT), str(TIMEOUT),
                        "cargo", "+capslock", "test", "--target=riscv64gc-unknown-linux-gnu",
                        "-p", package_name,
                    ]
                    + select_args
                    + [
                        "--",
                        "--test-threads", "1",
                        "--exact", test_name,
                        "-Z", "unstable-options",
                        "--format", "json"
                    ],
                    capture_output=True,
                    text=True,
                    start_new_session=True,
                    timeout=TIMEOUT
                )
            except:
                result = "timeout"
                summary = {}
                error_msgs = []
                exit_code = 0
            else:
                if p.returncode == 124:
                    result = "timeout"
                    summary = {}
                    error_msgs = []
                    exit_code = 0
                else:
                    # search in the output for the result
                    summary = {}
                    for l in p.stdout.splitlines():
                        try:
                            res = json.loads(l.strip())
                            if "passed" in res:
                                # ok we have found it
                                summary = res
                                break
                        except:
                            pass
                    # search in the error stream for violations
                    error_msgs = []
                    for l in p.stderr.splitlines():
                        if "invalid capability" in l or "OOB" in l or " assertion " in l:
                            error_msgs.append(l)
                    # if p.returncode != 0:
                    #     error_msgs = p.stderr.splitlines()
                    # print(p.stderr)
                    result = "finished"
                    exit_code = p.returncode
            capslock_result = {
                "result": result,
                "summary": summary,
                "errors": error_msgs,
                "exit_code": exit_code
            }

        test_results[full_test_name] = {
            "capslock": capslock_result,
            "miri": miri_result
        }

    # doing the clean up at last only
    subprocess.run(
        ["cargo", "+nightly", "clean"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    subprocess.run(
        ["cargo", "+capslock", "clean"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    os.chdir(cur_dir)

with open(test_results_file, "w") as fout:
    json.dump(test_results, fout, indent=2)
    # print(json.dumps(test_results, indent=2))

