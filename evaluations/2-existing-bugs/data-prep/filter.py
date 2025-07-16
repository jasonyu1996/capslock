import json

with open("pocs.json", "r") as fin:
    pocs = json.load(fin)

with open("db.json", "r") as fin:
    db = json.load(fin)

RELEVANT_CATEGORIES = ["memory-corruption", "memory-safe", "thread-safety"]
RELEVANT_KEYWORDS = ["memory", "thread", "race", "sound"]

def is_relevant(entry):
    keywords = ",".join(entry["advisory"].get("keywords", []))
    categories = entry["advisory"].get("categories", [])
    for c in RELEVANT_CATEGORIES:
        if c in categories:
            return True
    for k in RELEVANT_KEYWORDS:
        if k in keywords or k in entry["text"].lower():
            return True
    return False


relevant = []
for p, d in zip(pocs, db):
    assert(p["id"] == d["advisory"]["id"])
    if is_relevant(d):
        dn = d.copy()
        dn["likely_poc"] = p["likely_poc"]
        relevant.append(dn)

print("Found {} in total, out of which {} possibly have PoCs".format(len(relevant), len([d for d in relevant if d["likely_poc"]])))

with open("filtered.json", "w") as fout:
    json.dump(relevant, fout, indent=2)

