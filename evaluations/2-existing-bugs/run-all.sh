mkdir -p run-logs
(
    python3 << EOF
import json

with open("built.json", "r") as fin:
    li = json.load(fin)

for l in li:
    print(l)
EOF
) | parallel -j16 --bar 'sh run-user.sh {} > run-logs/{}.txt 2>&1'
