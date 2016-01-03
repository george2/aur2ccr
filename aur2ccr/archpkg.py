import sys
import os
import json
from html.parser import HTMLParser

import requests

SEARCH_URL = "https://www.archlinux.org/packages/search/json/?q="
PROJECTS_URL = "https://projects.archlinux.org/"
SRC_URL = PROJECTS_URL + "svntogit/packages.git/plain/{pkgname}/trunk/"
CHECK_URL = SRC_URL + "PKGBUILD"

def search(query):
    r = requests.get(SEARCH_URL + sys.argv[1])
    data = json.loads(r.text)
    return data['results']


def get_source_files(pkgname, workingdir="."):
    pkgdir = os.path.join(workingdir, pkgname)

    class HTMLLinkParser(HTMLParser):
        links = []
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        self.links.append(attr[1])

    r = requests.get(SRC_URL.format(pkgname=pkgname))
    # Raise if 404
    r.raise_for_status()
    p = HTMLLinkParser()
    p.feed(r.text)
    for link in p.links[1:]:
        data = requests.get(''.join([PROJECTS_URL, link])).text
        if not os.path.exists(pkgdir):
            os.mkdir(pkgdir)
        filename = os.path.join(pkgdir, link.split('/')[-1])
        with open(filename, 'w+') as f:
            f.write(data)

if __name__ == "__main__":
    for pkg in search(sys.argv[1]):
        print("{repo}/{name} {ver}\n    {desc}".format(
            repo = pkg['repo'],
            name = pkg['pkgname'],
            ver = pkg['pkgver'],
            desc = pkg['pkgdesc'],
        ))
    get_source_files(sys.argv[1])
