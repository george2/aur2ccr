__version__ = "2.0.1"

import argparse

from aur2ccr import aur2ccr

def main():
    parser = argparse.ArgumentParser(
            description="A helper script for porting packages from Arch to Chakra."
    )

    parser.add_argument('-v', '--version', action='version',
    		        help="show version information and exit",
		        version='aur2ccr {v}'.format(v=__version__))
    parser.add_argument('package', nargs='+',
			help='a package in the Arch repos or AUR')
    parser.add_argument('--search', action='store_true',
			help='search instead of downloading')

    args = parser.parse_args()
    if args.search:
        aur2ccr.search(' '.join(args.package))
    else:
        failed = []
        for pkg in args.package:
            failed += aur2ccr.get_all(pkg)
        if failed:
            print("Failed to download source packages for:")
            print("  {failed}".format(failed=' '.join(failed)))


if __name__ == "__main__":
    main()
