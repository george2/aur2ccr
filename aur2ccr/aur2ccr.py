import io
import tarfile
import subprocess
import json
import re
import os
import itertools

import requests
import ccr
import aur
from chaser import pacman

from aur2ccr import archpkg

SRC_URL = "https://aur.archlinux.org/cgit/aur.git/snapshot/{pkgname}.tar.gz"

def get_source_files(pkgname, workingdir="."):
    """Download the source tarball and extract it"""
    if not os.path.exists(workingdir):
        os.mkdir(workingdir)
    if os.path.exists(os.path.join(workingdir, pkgname)):
        # already exists locally, skip it
        return False

    try:
        archpkg.get_source_files(pkgname)
    except requests.exceptions.HTTPError:
        # Not in Arch repos, try AUR
        r = requests.get(SRC_URL.format(pkgname=pkgname))
        r.raise_for_status()
        tar = tarfile.open(mode='r', fileobj=io.BytesIO(r.content))
        tar.extractall(workingdir)

    return True

def recurse_depends(pkgname, graph=None):
    """Build a dependency graph"""
    if graph is None:
        graph = {}

    if graph.get(pkgname) is not None:
        # End case: already traversed
        return graph
    elif pacman.exists(pkgname):
        # End case: exists in pacman
        graph[pkgname] = set()
        return graph
    try:
        # End case: exists in ccr
        ccr.info(pkgname)
        graph[pkgname] = set()
        return graph
    except ccr.PackageNotFound:
        pass

    # Otherwise get dependencies
    graph[pkgname] = set()
    try:
        get_source_files(pkgname)
    except requests.exceptions.HTTPError:
        # Package not found, or other error
        return graph
    output = subprocess.check_output(["pkgvars.sh",
        "./{pkgname}/PKGBUILD".format(pkgname=pkgname)])
    data = json.loads(output.decode())['variables']
    # NOTE: We don't differentiate make/depends here, this is an area for
    # improvement in the future if someone cares.
    depends = data.get('makedepends', []) + data.get('depends', [])
    # Only depends that do not already exist
    for dep in depends:
        depname = re.split('[>=<]', dep)[0]
        if not pacman.exists(depname):
            try:
                ccr.info(depname)
            except ccr.PackageNotFound:
                graph[pkgname].add(depname)

    for dep in graph[pkgname]:
        recurse_depends(dep, graph)

    return graph

def dependency_chain(pkgname):
    """Return an ordered list of dependencies for a package"""
    depends = recurse_depends(pkgname)
    return set(list(depends.keys()) + list(itertools.chain.from_iterable(depends.values())))

def get_all(pkgname):
    """Get source files for pkgname and its missing dependencies"""
    failed = []
    print("downloading source files...")
    for pkg in dependency_chain(pkgname):
        try:
            get_source_files(pkg)
            print("{pkg}".format(pkg=pkg))
        except requests.exceptions.HTTPError:
            failed.append(pkg)

    return failed

def search(query):
    """Print search results"""
    archresults = archpkg.search(query)
    archresults.sort(key=lambda x: x['repo'] + x['pkgname'])
    for pkg in archresults:
        print("{repo}/{name} {ver}-{rel}\n    {desc}".format(
            repo = pkg['repo'],
            name = pkg['pkgname'],
            ver = pkg['pkgver'],
            rel = pkg['pkgrel'],
            desc = pkg['pkgdesc'],
        ))

    aurresults = aur.search(query)
    aurresults.sort(key=lambda x: x.name)
    for pkg in aurresults:
        print("aur/{name} {ver}".format(name=pkg.name, ver=pkg.version))
        print("    {desc}".format(desc=pkg.description))
