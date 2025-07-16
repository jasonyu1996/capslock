# Look at files in logs-new to print out stats

import pathlib, json, sys, os
import collections
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# These are manually checked to be failing due to environment problems (missing files).
# We exclude them from the results
ENV_SKIP = """all>rustc_error
all>smoketest
namedtempfile>test_make_uds_conflict
>tests::test_parse_current
no_std>no_std
rustflags>test_with_sysroot
tests>autocfg_version
tests>probe_add
tests>probe_alloc
tests>probe_as_ref
tests>probe_bad_sysroot_crate
tests>probe_constant
tests>probe_expression
tests>probe_i128
tests>probe_no_std
tests>probe_raw
tests>probe_std
tests>probe_sum
wrappers>test_wrappers
compiletest>ui"""
ENV_SKIP = set(ENV_SKIP.splitlines())


# These test cases do not trigger either capslock or miri detection,
# fail assertions, but are manually checked to behave correctly.
# Discrepancies are due to the different environments.
ENV_PASS="""test_ensure>test_closure
test_ensure>test_if
test_ensure>test_loop
test_ensure>test_match
test_ensure>test_path"""
ENV_PASS = set(ENV_PASS.splitlines())

def get_capslock_result(raw_result):
    if raw_result["result"] == "finished":
        if raw_result["summary"].get("event", "") == "ok":
            return ("ok", raw_result["summary"]["exec_time"])
        else:
            # look at the errors
            for e in raw_result["errors"]:
                if "invalid capability" in e:
                    return ("invalid-cap", 0)
                elif "OOB" in e:
                    return ("oob", 0)
            return ("others", 0)
    elif raw_result["result"] == "timeout":
        return ("timeout", 0)
    else:
        raise Exception("Unknown capslock result")

def get_miri_result(raw_result):
    if raw_result["result"] == "finished":
        if raw_result["summary"].get("event", "") == "ok":
            return ("ok", raw_result["summary"]["exec_time"])
        else:
            for e in raw_result["errors"]:
                if "unsupported operation" in e:
                    return ("unsupported", 0)
            return ("others", 0)
    elif raw_result["result"] == "timeout":
        return ("timeout", 0)
    elif raw_result["result"] == "ignored":
        return ("ignored", 0)
    else:
        raise Exception("Unknown miri result")

if len(sys.argv) > 1:
    logs_dir = pathlib.Path(sys.argv[1])
else:
    logs_dir = pathlib.Path("./logs-new")

counter = collections.Counter()
time_list = []

for log_file in logs_dir.glob("*.json"):
    with open(log_file, "r") as fin:
        try:
            test_results = json.load(fin)
        except:
            test_results = {}
    for full_case_name, case_result in test_results.items():
        if full_case_name in ENV_SKIP:
            continue
        (capslock_res, capslock_time) = get_capslock_result(case_result["capslock"])
        (miri_res, miri_time) = get_miri_result(case_result["miri"])

        if (capslock_res == "others" or miri_res == "others") and full_case_name in ENV_PASS:
            counter.update([("ok", "ok")])
            continue

        if capslock_res != "timeout" and miri_res != "timeout":
            counter.update([(capslock_res, miri_res)])
            if capslock_res == "ok" and miri_res == "ok":
                time_list.append((capslock_time, miri_time))


# Print out statistics

print("Total cases: {}".format(counter.total()))

miri_counter = collections.Counter()

for capslock_res, capslock_label in zip(["ok", "oob", "invalid-cap", "others"],
                                        ["\\textbf{\\codename{} P}", "\\textbf{\\codename{} F (OOB)}",
                                        "\\textbf{\\codename{} F (invalid cap)}", "\\textbf{\\codename{} F (others)}"]):
    print("{} ".format(capslock_label), end="")
    tot = 0
    for miri_res in ["ok", "ignored", "unsupported", "others"]:
        tot += counter[(capslock_res, miri_res)]
        miri_counter[miri_res] += counter[(capslock_res, miri_res)]
        print("& {} ".format(counter[(capslock_res, miri_res)]), end="")
    print("& {} \\\\".format(tot))
    if capslock_res == "ok":
        passed_tot = tot

print("\\textbf{Total} ", end="")
for miri_res in ["ok", "ignored", "unsupported", "others"]:
    print("& {} ".format(miri_counter[miri_res]), end="")
print("& {} \\\\".format(miri_counter.total()))

print("Passed = {}/{} ({}%)".format(passed_tot, miri_counter.total(),
                                    passed_tot / miri_counter.total() * 100))

time_ratio = [capslock_time / miri_time for capslock_time, miri_time in time_list]
lower_count = len(list(filter(lambda x: x < 1, time_ratio)))
print("Performance Average = {}%".format(np.mean(time_ratio) * 100))

# if len(sys.argv) > 1 and sys.argv[1] == "draw":
if "DRAW" in os.environ:
    # draw a histogram
    plt.figure(figsize=(3, 3))
    plt.hist(time_ratio, bins=100, range=(0, 1.0))
    plt.ylabel("# of test cases")
    plt.xlabel("CapsLock time / MIRI time")
    plt.gca().set_aspect(0.0008)
    plt.savefig("performance-hist.pdf", bbox_inches="tight")
