#!/usr/bin/python3

from PySide import QtCore, QtGui, QtWebKit, QtNetwork
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

	def waitUntilReady(self) :
		while not w.initialized :
			QtCore.QCoreApplication.processEvents()

	def onLoadFinished(self, ok) :
		if self.initialized : return
		if not ok : return
		self.initialized = True
		self.centerAt(0,0)
		self.setZoom(1)
#		self.centerAt(41.35,2.05)
#		self.setZoom(13)

	def runScript(self, script) :
		self.page().mainFrame().evaluateJavaScript(script)


	def centerAt(self, latitude, longitude) :
		self.runScript("setGMapCenter({},{})".format(latitude, longitude))

	def setZoom(self, zoom) :
		self.runScript("setGMapZoom({})".format(zoom))

	def centerAtAddress(self, location) :
		
		url = QtCore.QUrl("http://maps.googleapis.com/maps/api/geocode/xml")
		url.addQueryItem("address", location)
		url.addQueryItem("sensor", "false")

		request = QtNetwork.QNetworkRequest(url)
		self._accessManager().get(request)

	def _accessManager(self) :
		"""Lazy initializer for the network access manager"""
		if not hasattr(self, "_connectionManager") :
			self._connectionManager = QtNetwork.QNetworkAccessManager(self)
			self._connectionManager.finished.connect(self.geocodeReturned)
		return self._connectionManager

	def geocodeReturned(self, reply) :
		xml = reply.readAll()
		print (xml)
		reader = QtCore.QXmlStreamReader(xml)
		while not reader.atEnd() :
			reader.readNext()
			print ("X",reader.name())
			if reader.name() != "geometry" : continue
			print (reader.name())
			reader.readNextStartElement()
			if reader.name() != "location" : continue
			print (reader.name())
			reader.readNextStartElement()
			if reader.name() != "lat" : continue
			print (reader.name())
			latitude = float(reader.readElementText())
			reader.readNextStartElement()
			if reader.name() != "lng" : continue
			print (reader.name())
			longitude = float(reader.readElementText())
			self.centerAt(latitude, longitude)
			return


if __name__ == '__main__' :

	app = QtGui.QApplication([])
	w = QGoogleMap()
	w.show()
	w.waitUntilReady()
	w.centerAtAddress("Verdaguer 40, Sant Joan Despí")
	w.setZoom(17)

	app.exec_()



