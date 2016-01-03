import os
from setuptools import setup

from aur2ccr import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aur2ccr',
    version=__version__,
    packages=['aur2ccr'],
    entry_points = {
        'console_scripts': ['aur2ccr = aur2ccr:main'],
    },
    include_package_data=True,
    install_requires=[],
    license='BSD',
    description='A helper script for porting packages from Arch to Chakra',
    long_description=README,
    url='https://github.com/ccr-tools/aur2ccr',
    author='Ryan Shipp',
    author_email='python@rshipp.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Software Distribution',
    ],
)
