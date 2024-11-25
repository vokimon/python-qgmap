
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

class CustomUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
	def interceptRequest(self, request):
		return
		print(f"Accessing: {request.requestUrl().toString()}")

class LocalWebPage(QtWebEngineCore.QWebEnginePage):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.interceptor = CustomUrlRequestInterceptor()
		self.web_engine_profile = QtWebEngineCore.QWebEngineProfile.defaultProfile()
		self.web_engine_profile.setUrlRequestInterceptor(self.interceptor)

	@trace
	def javaScriptConsoleMessage(self, level, msg, line, source):
		print ('JS: %s %d: %s' % (source, line, msg))


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
	def __init__(self, parent):
		super().__init__(parent)
		"""
		QtWebEngineCore.QWebEngineSettings.globalSettings().setAttribute(
		"""
		self.setPage(LocalWebPage())
		S = QtWebEngineCore.QWebEngineSettings
		settings = {
			#S.DeveloperExtrasEnabled: True, # Legacy?
			S.AutoLoadImages: True,
			S.JavascriptCanAccessClipboard: True,
			S.ForceDarkMode: True,
			S.LocalContentCanAccessRemoteUrls: True,
			#S.LocalContentCanAccessFileUrls: True,
		}
		for attribute, value in settings.items():
			self.settings().setAttribute(attribute, value)

		self.initialized = False
		self.resize(1024, 750);
		self.loadFinished.connect(self.onLoadFinished)
		self.page().loadingChanged.connect(
			lambda info:
				print(
					f"Loading {info.url().toString()}...\n"
					f"\t{info.errorString()}"
				)
		)
		self.channel = QtWebChannel.QWebChannel(self)
		self.page().setWebChannel(self.channel)
		self.channel.registerObject('qtWidget', self)

		basePath=os.path.abspath(os.path.dirname(__file__))
		url = 'file://'+basePath+'/qgmap.html'
		self.load(QtCore.QUrl(url))


	def closeEvent(self, event):
		# Ensure proper interceptor cleanup when the window is closed
		self.interceptor = None
		super().closeEvent(event)


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
		self.runScript(f"gmap_setCenter({latitude},{longitude})")

	@trace
	def setZoom(self, zoom) :
		self.runScript(f"gmap_setZoom({zoom})")

	@trace
	def center(self) :
		return self.runScript("gmap_getCenter()")

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
			f"gmap_addMarker({key!r}, {latitude}, {longitude}, {extra})"
		)

	@trace
	def moveMarker(self, key, latitude, longitude) :
		return self.runScript(
			f"gmap_moveMarker({key!r}, {latitude}, {longitude})"
		)

	@trace
	def setMarkerOptions(self, key, **extra) :
		return self.runScript(
			f"gmap_changeMarker({key!r}, {extra})"
		)

	@trace
	def deleteMarker(self, key) :
		return self.runScript(
			f"gmap_deleteMarker({key!r})"
		)

	@trace
	def setTileSet(self, tilesetOptions) :
		return self.runScript(
			f"gmap_setTileSet({tilesetOptions})"
		)

	mapMoved = QtCore.Signal(float, float)
	mapClicked = QtCore.Signal(float, float)
	mapRightClicked = QtCore.Signal(float, float)
	mapDoubleClicked = QtCore.Signal(float, float)

	markerMoved = QtCore.Signal(str, float, float)
	markerClicked = QtCore.Signal(str, float, float)
	markerDoubleClicked = QtCore.Signal(str, float, float)
	markerRightClicked = QtCore.Signal(str, float, float)

	# Hack to emit signals from JS, should not be needed

	@QtCore.Slot(float, float)
	def emitMapMoved(self, lat: float, lng: float):
		self.mapMoved.emit(lat, lng)

	@QtCore.Slot(float, float)
	def emitMapClicked(self, lat: float, lng: float):
		self.mapClicked.emit(lat, lng)

	@QtCore.Slot(float, float)
	def emitMapDoubleClicked(self, lat: float, lng: float):
		self.mapDoubleClicked.emit(lat, lng)

	@QtCore.Slot(float, float)
	def emitMapRightClicked(self, lat: float, lng: float):
		self.mapRightClicked.emit(lat, lng)

	@QtCore.Slot(str, float, float)
	def emitMarkerMoved(self, key: str, lat: float, lng: float):
		self.markerMoved.emit(key, lat, lng)

	@QtCore.Slot(str, float, float)
	def emitMarkerClicked(self, key: str, lat: float, lng: float):
		self.markerClicked.emit(key, lat, lng)

	@QtCore.Slot(str, float, float)
	def emitMarkerDoubleClicked(self, key: str, lat: float, lng: float):
		self.markerDoubleClicked.emit(key, lat, lng)

	@QtCore.Slot(str, float, float)
	def emitMarkerRightClicked(self, key: str, lat: float, lng: float):
		self.markerRightClicked.emit(key, lat, lng)


# set ts=4 sw=4 noet
