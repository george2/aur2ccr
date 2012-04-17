#!/usr/bin/env python2

from __future__ import print_function
from __future__ import unicode_literals

import argparse


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Usage: aur2ccr [OPTIONS] [PACKAGES]\n"
            "Create CCR-ready source packages from packages in AUR or Arch repos",
            epilog="Report bugs at"
            ": <https://github.com/ccr-tools/aur2ccr/issues/>\n"
            "aur2ccr home: <https://github.com/ccr-tools/aur2ccr/>")
    parser.add_argument("--maintainer", "-m", help="add maintainer information"
            "to each PKGBUILD before building")
    parser.add_argument("-e", "--edit",
            help="edit the PKGBUILD for each package with $EDITOR before building",
            action="store_true")
    parser.add_argument("-c", "--consolidate", help="move all CCR source packages"
            "into the working directory", action="store_true")
    parser.add_argument("-i", "--install", help="install packages that build "
            "successfully, in order to test them", action="store_true")
    parser.add_argument("-f", "--from-src", help="create a CCR source package "
            "from source package <file>", metavar="<file>")
    parser.add_argument("-u", "--from-url", metavar="<url>",
            help="... or from an AUR/CCR-compatible source package at <URL>")
    parser.add_argument("-d", "--from-dir", metavar="<dir>",
            help="...or from a PKGBUILD and (optional) other files in <dir>")
    parser.add_argument("-C", "--cd", metavar="<newdir>",
            help="use <newdir> as the working directory instead of the current dir")
    parser.add_argument("-t", "--temp", help="use $tmpdir as the build directory"
            "instead of the current dir (all finished src packgages will be "
            "moved into the current dir, like -c)", action="store_true")
    parser.add_argument("-l", "--log", metavar="<logfile>",
            help="log all messages from aur2ccr in <logfile>")
    parser.add_argument("-s", "--setup", action="store_true",
            help="perform setup related tasks (not required)")
    parser.add_argument("-a", "--addad", action="store_true",
            help="add an aur2ccr advertisment - as an Contributor")
    parser.add_argument("-v", "--version", action="store_true",
            help="print version information and exit")
    return parser


if __name__ == "__main__":
    parser = main()
    parser.parse_args()
