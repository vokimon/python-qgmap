#!/usr/bin/python3

from PySide import QtCore, QtGui, QtWebKit
import os


class QGoogleMap(QtWebKit.QWebView) :
	pass


basePath=os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__' :
	app = QtGui.QApplication([])

	w = QGoogleMap()
	url = 'file://'+basePath+'/qgmap.html'
	w.load(url)
	w.show()

	app.exec_()

