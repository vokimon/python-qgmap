#!/usr/bin/python3
from distutils.core import setup
import sys
import os

if not os.access("README.rst", os.F_OK) :
	print("Generate README.rst, from README.md using pandoc:\n\t$ pandoc README.md -o README.rst", file=sys.stderr)
	sys.exit(-1)

setup(
	name = "qgmap",
	version = "1.0",
	description = "Google Map widget for PySyde/PyQt4",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/vokimon/python-qgmap',
	long_description = open('README.rst').read(),
	license = 'GNU General Public License v3 or later (GPLv3+)',
	packages=[
		'qgmap',
		],
	scripts=[
		'qgmap-example.py',
		],
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: GIS',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Environment :: X11 Applications :: Qt',
		'Environment :: Win32 (MS Windows)',
		'Intended Audience :: Developers',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
	)

