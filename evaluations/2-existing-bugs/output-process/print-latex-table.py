import csv
import collections

counter = collections.Counter()
counter_separate = [collections.Counter() for _ in range(4)]
counter_separate_strict = [collections.Counter() for _ in range(4)]

rows = []

with open("experiments.csv", "r", newline='') as fin:
    reader = csv.DictReader(fin)
    for row in reader:
        if row["Relevant"] != "Y":
            continue
        def check_detected(col_name):
            s = row[col_name]
            if s == "Y":
                return "\\cmark"
            elif s == "Y (as UAF)":
                return "UAF"
            elif s == "Y (memleak)":
                return "ML"
            elif s == "Y (Invalid addr)":
                return "IA"
            elif s == "Y (double free)":
                return "DF"
            elif s == "Y (OOB)":
                return "OF"
            elif s == "Y (assume called with false)":
                # TODO: what to do with this?
                return "\\cmark"
            elif s == "N":
                return "\\xmark"
            else:
                return ""
        detected = check_detected("Detected")
        asan = check_detected("AddressSanitizer")
        tsan = check_detected("ThreadSanitizer")
        miri = check_detected("MIRI")

        cause = row["Cause (succinct)"]
        cause = cause.replace(" (heap)", "")
        cause = cause.replace(" (stack)", "")
        counter[cause] += 1
        for c, cs, v in zip(counter_separate, counter_separate_strict, [detected, asan, tsan, miri]):
            if v and v != "\\xmark":
                c[cause] += 1
            if v == "\\cmark":
                cs[cause] += 1
        rows.append((row["RustSec ID"], row["Crate"].replace(")", "").replace("(", ""), cause, detected, asan, tsan, miri))

for r in sorted(rows, key=lambda x: x [2]):
    print("{} & \\verb|{}| & {} & {} & {} & {} & {} \\\\"
        .format(*r))

for c in counter:
    print("{} & {} ".format(c, counter[c]), end="")
    for cr, cs in zip(counter_separate, counter_separate_strict):
        # print("& {} & {} ".format(cr[c], cs[c]), end="")
        print("& {} ".format(cr[c]), end="")
    print("\\\\")

print("Total & {} ".format(counter.total()), end="")
for cr, cs in zip(counter_separate, counter_separate_strict):
    # print("& {} & {} ".format(cr.total(), cs.total()), end="")
    print("& {} ".format(cr.total()), end="")
print("\\\\")
