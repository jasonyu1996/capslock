import sys
import tomllib
import json
import re

toml_re = re.compile('```toml(.+?)```', re.DOTALL)
all_vulns = []

for file_name in sys.argv[1:]:
    print("Parsing {} ...".format(file_name))
    with open(file_name, "r") as fin:
        s = fin.read()
        m = toml_re.search(s)
        toml_str = m.group(1)
        attributes = tomllib.loads(toml_str.strip())
        attributes["text"] = s[m.end(0):]
        all_vulns.append(attributes)

with open("db.json", "w") as fout:
    json.dump(all_vulns, fout, indent=2)
