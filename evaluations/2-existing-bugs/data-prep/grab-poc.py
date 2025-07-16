import json
import re
import time
import urllib.request

with open("db.json", "r") as fin:
    db = json.load(fin)

class JsonWalker:
    def visit_string(self, s):
        raise NotImplementedError()

    def visit_obj(self, o):
        if isinstance(o, dict):
            for on in o.values():
                self.visit_obj(on)
        elif isinstance(o, list):
            for on in o:
                self.visit_obj(on)
        elif isinstance(o, str):
            self.visit_string(o)
        else:
            raise NotImplementedError()

class UrlGrabber(JsonWalker):
    # URLREGEX = re.compile('https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

    def __init__(self):
        self.urls = []

    def visit_string(self, s):
        if s.startswith("http://") or s.startswith("https://"):
            self.urls.append(s)

PRETAG = re.compile('<pre[ >]', re.IGNORECASE)

outd = []

for entry in db:
    url_grabber = UrlGrabber()
    url_grabber.visit_obj(entry)
    likely_poc = []
    try:
        for u in url_grabber.urls:
            contents = urllib.request.urlopen(u).read()
            if re.search(PRETAG, contents.decode()):
                likely_poc.append(u)
            time.sleep(.1)
    except:
        print("Failed to load {}".format(u))
    print("{}: {}".format(entry["advisory"]["id"], likely_poc))
    outd.append({"id": entry["advisory"]["id"], "likely_poc": likely_poc})

with open("pocs.json", "w") as fout:
    json.dump(outd, fout, indent=2)


