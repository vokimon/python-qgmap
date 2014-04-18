#!/usr/bin/python3

from PySide import QtCore, QtGui, QtWebKit
import os


class LoggedPage(QtWebKit.QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        print ('JS: %s line %d: %s' % (source, line, msg))

class QGoogleMap(QtWebKit.QWebView) :
	def __init__(self) :
		super(QGoogleMap, self).__init__()
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
		self.setPage(LoggedPage())

	pass


basePath=os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__' :
	app = QtGui.QApplication([])

	w = QGoogleMap()
	url = 'file://'+basePath+'/qgmap.html'
	w.load(url)
	w.show()

	app.exec_()

