import json

with open("db.json", "r") as fin:
    db = json.load(fin)

with open("built.json", "r") as fin:
    built_l = json.load(fin)


db = dict([(d["advisory"]["id"], d) for d in db])

RELEVANT_KEYWORDS = ["memory", "thread", "race", "sound"]

CLASSES = [
    (["race", "thread", "concurrency"], "thread"),
    (["use-after-free", "double-free", "double free", "use-after-free"], "temporal"),
    (["memory"], "memory"),
    (["sound"], "soundness"),
]

def classify(s):
    for cls_keywords, cls_name in CLASSES:
        for w in cls_keywords:
            if w in s:
                return cls_name
    return "unknown"

for entry in built_l:
    e = db[entry]
    text = e["text"].lower()
    v = filter(lambda w: w in text, RELEVANT_KEYWORDS)
    metadata = "[{}] [{}] [{}]".format(
                                ",".join(e["advisory"].get("categories", [])),
                                ",".join(e["advisory"].get("keywords", [])),
                                ",".join(v))
    cls = classify(metadata)
    print("{}: {} (class = {})".format(entry, metadata, cls))
