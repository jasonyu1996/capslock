import json
import subprocess, tempfile
import signal

SAVE_FILE_NAME = "saved.json"

saved = []

def save():
    with open(SAVE_FILE_NAME, "w") as fout:
        json.dump(saved, fout, indent=2)

def sighandler(signum, frame):
    assert(signal.SIGINT == signum)
    print("Saving and exiting ...")
    save()
    exit(0)

signal.signal(signal.SIGINT, sighandler)

with open("filtered.json", "r") as fin:
    db = json.load(fin)

try:
    with open(SAVE_FILE_NAME, "r") as fin:
        saved = json.load(fin)
except:
    pass

bypass_ids = set([d["id"] for d in saved])

# skipping already-saved ones
for idx, entry in enumerate(db):
    if entry["advisory"]["id"] in bypass_ids:
        continue
    if entry["likely_poc"]:
        info_lines =  \
            [
                "{} out of {}".format(idx, len(db)),
                "Package: {}".format(entry["advisory"]["package"]),
                "Keywords: {}".format(", ".join(entry["advisory"].get("keywords", []))),
                "URLs: {}".format(" ".join(entry["likely_poc"])),
                "Patched: {}".format(",".join(entry["versions"].get("patched", []))),
                "Unaffected: {}".format(",".join(entry["versions"].get("unaffected", [])))
            ]
        with tempfile.NamedTemporaryFile("w", suffix=".rs", delete_on_close=False) as tempf:
            tempf.write(
                "\n".join(["// " + l for l in info_lines] + ["// ## END OF HEADER ##", "", ""])
            )
            tempf.close()
            subprocess.run(["vim", "-c", "normal G", tempf.name])
            with open(tempf.name, "r") as fin:
                for line in fin:
                    if "## END OF HEADER ##" in line:
                        break
                poc = fin.read()
                if not poc.strip(" \t\r\n"):
                    poc = ""
        print("\n".join(info_lines))
        version_poc = input("Version for PoC = ")
        saved.append({"id": entry["advisory"]["id"], "poc": poc, "version_poc": version_poc})
    else:
        saved.append({"id": entry["advisory"]["id"], "poc": "", "version_poc": ""})

save()
