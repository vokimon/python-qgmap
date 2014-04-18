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

		self.loadFinished.connect(self.onLoadFinished)

		self.initialized = False

		basePath=os.path.abspath(os.path.dirname(__file__))
		url = 'file://'+basePath+'/qgmap.html'
		self.load(url)


	def onLoadFinished(self, ok) :
		if self.initialized : return
		if not ok : return
		self.initialized = True
		self.centerAt(41.35,2.05)
		self.setZoom(13)

	def runScript(self, script) :
		self.page().mainFrame().evaluateJavaScript(script)


	def centerAt(self, latitude, longitude) :
		self.runScript("setGMapCenter({},{})".format(latitude, longitude))

	def setZoom(self, zoom) :
		self.runScript("setGMapZoom({})".format(zoom))




if __name__ == '__main__' :


	app = QtGui.QApplication([])
	w = QGoogleMap()
	w.show()

	app.exec_()

