#!/usr/bin/python3

doTrace = False
usePySide = True
if usePySide :
	from PySide import QtCore, QtGui, QtWebKit, QtNetwork
else :
	from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
	QtCore.Signal = QtCore.pyqtSignal
	QtCore.Slot = QtCore.pyqtSlot
	QtCore.Property = QtCore.pyqtProperty

import json
import os
import decorator


@decorator.decorator
def trace(function, *args, **k) :
	"""Decorates a function by tracing the begining and
	end of the function execution, if doTrace global is True"""

	if doTrace : print ("> "+function.__name__, args, k)
	result = function(*args, **k)
	if doTrace : print ("< "+function.__name__, args, k, "->", result)
	return result

class _LoggedPage(QtWebKit.QWebPage):
	@trace
	def javaScriptConsoleMessage(self, msg, line, source):
		print ('JS: %s line %d: %s' % (source, line, msg))

class GeoCoder(QtNetwork.QNetworkAccessManager) :
	class NotFoundError(Exception) : pass

	@trace
	def __init__(self, parent) :
		super(GeoCoder, self).__init__(parent)

	@trace
	def geocode(self, location) :
		url = QtCore.QUrl("http://maps.googleapis.com/maps/api/geocode/xml")
		url.addQueryItem("address", location)
		url.addQueryItem("sensor", "false")
		"""
		url = QtCore.QUrl("http://maps.google.com/maps/geo/")
		url.addQueryItem("q", location)
		url.addQueryItem("output", "csv")
		url.addQueryItem("sensor", "false")
		"""
		request = QtNetwork.QNetworkRequest(url)
		reply = self.get(request)
		while reply.isRunning() :
			QtGui.QApplication.processEvents()

		reply.deleteLater()
		self.deleteLater()
		return self._parseResult(reply)

	@trace
	def _parseResult(self, reply) :
		xml = reply.readAll()
		reader = QtCore.QXmlStreamReader(xml)
		while not reader.atEnd() :
			reader.readNext()
			if reader.name() != "geometry" : continue
			reader.readNextStartElement()
			if reader.name() != "location" : continue
			reader.readNextStartElement()
			if reader.name() != "lat" : continue
			latitude = float(reader.readElementText())
			reader.readNextStartElement()
			if reader.name() != "lng" : continue
			longitude = float(reader.readElementText())
			return latitude, longitude
		raise NotFoundError


class QGoogleMap(QtWebKit.QWebView) :

	@trace
	def __init__(self, parent, debug=True) :
		super(QGoogleMap, self).__init__(parent)
		if debug :
			QtWebKit.QWebSettings.globalSettings().setAttribute(
				QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
			self.setPage(_LoggedPage())

		self.initialized = False
		self.loadFinished.connect(self.onLoadFinished)
		self.page().mainFrame().addToJavaScriptWindowObject(
			"qtWidget", self)

		basePath=os.path.abspath(os.path.dirname(__file__))
		url = 'file://'+basePath+'/qgmap.html'
		self.load(QtCore.QUrl(url))

	@trace
	def onLoadFinished(self, ok) :
		if self.initialized : return
		if not ok :
			print("Error initializing Google Maps")
		self.initialized = True
		self.centerAt(0,0)
		self.setZoom(1)

	@trace
	def waitUntilReady(self) :
		while not self.initialized :
			QtGui.QApplication.processEvents()

	@trace
	def geocode(self, location) :
		return GeoCoder(self).geocode(location)

	@trace
	def runScript(self, script) :
		return self.page().mainFrame().evaluateJavaScript(script)

	@trace
	def centerAt(self, latitude, longitude) :
		self.runScript("setGMapCenter({},{})".format(latitude, longitude))

	@trace
	def setZoom(self, zoom) :
		self.runScript("setGMapZoom({})".format(zoom))

	@trace
	def centerAtAddress(self, location) :
		try : latitude, longitude = self.geocode(location)
		except GeoCoder.NotFoundError : return None
		self.centerAt(latitude, longitude)
		return latitude, longitude

	@trace
	def markerAtAddress(self, location, **extra) :
		try : latitude, longitude = self.geocode(location)
		except GeoCoder.NotFoundError : return None
		return self.addMarker(location, latitude, longitude, **extra)
		


	@trace
	def addMarker(self, key, latitude, longitude, **extra) :
		return self.runScript(
			"addGMapMarker("
				"key={!r}, "
				"latitude={}, "
				"longitude={}, "
				"{}"
				"); "
				.format( key, latitude, longitude, json.dumps(extra)))

	markerMoved = QtCore.Signal(str, float, float)

if __name__ == '__main__' :

	def goCoords() :
		try : latitude, longitude = coordsEdit.text().split(",")
		except ValueError : pass
		else : gmap.centerAt(latitude, longitude)
	def goAddress() :
		coords = gmap.centerAtAddress(addressEdit.text())

	app = QtGui.QApplication([])
	w = QtGui.QDialog()
	l = QtGui.QFormLayout(w)
	gmap = QGoogleMap(w)

	coordsEdit = QtGui.QLineEdit()
	l.addRow('Coords:', coordsEdit)
	coordsEdit.editingFinished.connect(goCoords)
	addressEdit = QtGui.QLineEdit()
	l.addRow('Address:', addressEdit)
	addressEdit.editingFinished.connect(goAddress)
	l.addRow(gmap)
	w.show()
	gmap.waitUntilReady()
	gmap.centerAt(41.35,2.05)
	gmap.setZoom(13)
	coords = gmap.centerAtAddress("Major 3, Santa Coloma de Cervelló")
	gmap.addMarker("MyDragableMark", *coords, **dict(
		icon="http://google.com/mapfiles/ms/micons/blue-dot.png",
		draggable=True,
		))

	gmap.markerAtAddress("Major 13, Santa Coloma de Cervelló",
		icon="http://google.com/mapfiles/ms/micons/green-dot.png",
		draggable=True,
		)

	gmap.setZoom(17)

	def onMarkerMoved(key, latitude, longitude) :
		print("Moved!!", key, latitude, longitude)

	gmap.markerMoved.connect(onMarkerMoved)


	app.exec_()



