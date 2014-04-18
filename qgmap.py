#!/usr/bin/python3

from PySide import QtCore, QtGui, QtWebKit
import os

class LoggedPage(QtWebKit.QWebPage):
	def javaScriptConsoleMessage(self, msg, line, source):
		print ('JS: %s line %d: %s' % (source, line, msg))


class QGoogleMap(QtWebKit.QWebView) :

	def __init__(self, debug=True) :
		super(QGoogleMap, self).__init__()
		if debug :
			QtWebKit.QWebSettings.globalSettings().setAttribute(
				QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
			self.setPage(LoggedPage())
		basePath=os.path.abspath(os.path.dirname(__file__))
		url = 'file://'+basePath+'/qgmap.html'
		self.load(url)




if __name__ == '__main__' :


	app = QtGui.QApplication([])
	w = QGoogleMap()
	w.show()

	app.exec_()

