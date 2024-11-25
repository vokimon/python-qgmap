
doTrace = False
usePySide = True
if usePySide :
	from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets, QtWebChannel, QtNetwork
else :
	from PyQt6 import QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets, QtWebChannel, QtNetwork
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

class _LoggedPage(QtWebEngineCore.QWebEnginePage):
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
		#url = QtCore.QUrl("http://maps.googleapis.com/maps/api/geocode/xml")
		url = QtCore.QUrl(
			"https://nominatim.openstreetmap.org/search")
		query = QtCore.QUrlQuery()
		query.addQueryItem("q", location)
		query.addQueryItem("format", "json")
		query.addQueryItem("polygon", "1")
		query.addQueryItem("addressdetails", "1")
		url.setQuery(query)
		request = QtNetwork.QNetworkRequest(url)
		reply = self.get(request)
		while reply.isRunning() :
			QtWidgets.QApplication.processEvents()

		reply.deleteLater()
		self.deleteLater()
		return self._parseResult(reply)

	@trace
	def _parseResult(self, reply) :
		jsondata = reply.readAll()
		data = json.loads(bytes(jsondata))
		if not data: raise GeoCoder.NotFoundError
		return data[0]['lat'], data[0]['lon']

class QGoogleMap(QtWebEngineWidgets.QWebEngineView) :

	@trace
	def __init__(self, parent, debug=True) :
		super(QGoogleMap, self).__init__(parent)
		if debug :
			"""
			QtWebEngineCore.QWebEngineSettings.globalSettings().setAttribute(
				QtWebEngineCore.QWebEngineSettings.DeveloperExtrasEnabled, True)
			"""
			self.setPage(_LoggedPage())

		self.initialized = False
		self.loadFinished.connect(self.onLoadFinished)
		self.channel = QtWebChannel.QWebChannel(self)
		self.page().setWebChannel(self.channel)
		self.channel.registerObject('qtWidget', self)

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
			QtWidgets.QApplication.processEvents()

	@trace
	def geocode(self, location) :
		return GeoCoder(self).geocode(location)

	@trace
	def runScript(self, script) :
		return self.page().runJavaScript(script)

	@trace
	def centerAt(self, latitude, longitude) :
		self.runScript("gmap_setCenter({},{})".format(latitude, longitude))

	@trace
	def setZoom(self, zoom) :
		self.runScript("gmap_setZoom({})".format(zoom))

	@trace
	def center(self) :
		center = self.runScript("gmap_getCenter()")
		return center.lat, center.lng

	@trace
	def centerAtAddress(self, location) :
		try : latitude, longitude = self.geocode(location)
		except GeoCoder.NotFoundError : return None
		self.centerAt(latitude, longitude)
		return latitude, longitude

	@trace
	def addMarkerAtAddress(self, location, **extra) :
		if 'title' not in extra :
			extra['title'] = location
		try : latitude, longitude = self.geocode(location)
		except GeoCoder.NotFoundError : return None
		return self.addMarker(location, latitude, longitude, **extra)

	@trace
	def addMarker(self, key, latitude, longitude, **extra) :
		return self.runScript(
			"gmap_addMarker("
				"key={!r}, "
				"latitude={}, "
				"longitude={}, "
				"{}"
				"); "
				.format( key, latitude, longitude, json.dumps(extra)))

	@trace
	def moveMarker(self, key, latitude, longitude) :
		return self.runScript(
			"gmap_moveMarker({!r}, {}, {});".format(key,latitude,longitude))

	@trace
	def setMarkerOptions(self, keys, **extra) :
		return self.runScript(
			"gmap_changeMarker("
				"key={!r}, "
				"{}"
				"); "
				.format( keys, json.dumps(extra)))

	@trace
	def deleteMarker(self, key) :
		return self.runScript(
			"gmap_deleteMarker("
				"key={!r} "
				"); "
				.format( key))

	mapMoved = QtCore.Signal(float, float)
	mapClicked = QtCore.Signal(float, float)
	mapRightClicked = QtCore.Signal(float, float)
	mapDoubleClicked = QtCore.Signal(float, float)

	markerMoved = QtCore.Signal(str, float, float)
	markerClicked = QtCore.Signal(str)
	markerDoubleClicked = QtCore.Signal(str)
	markerRightClicked = QtCore.Signal(str)



