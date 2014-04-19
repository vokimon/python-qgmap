python-gmap
===========

Qt Google Map widget for PySide/PyQt4

## Installation

By using pypi:

	$ pypi-install python-qgmap

From source:

	python3 setup.py --install

## Usage

Two main classes are provided:

- qgmap.GeoCoder:
	Retrieves geo-coordinates (latitude, longitude) from street addresses
- qgmap.QGoogleMap:
	A WebView widget containing a GoogleMap, with some convenience accessors
	to manage center, zoom, markers...


See the main example code at qgmap-example.py

## Using it with PyQt4

By default the classes use PySide, but the code works for PyQt4 if you
set to False the usePySide module variable by hand.

Any suggestion to make this less hacky is welcome.

## Acknoledgements

This Python code has been inspired in Henrik Hartz's C++ code:

	https://blog.qt.digia.com/blog/2008/07/03/putting-qtwebkit-to-use-with-google-maps/


