#!/usr/bin/python 

from PySide import QtCore, QtGui, QtWebKit


class QGoogleMap(QtWebKit.QWebView) :
	pass



if __name__ == '__main__' :
	app = QtGui.QApplication([])

	w = QGoogleMap()
	w.load("http://maps.google.com")
	w.show()

	app.exec_()

