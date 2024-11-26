import os
from pathlib import Path
from .geocoder import GeoCoder
from .qt import QtCore, QtWidgets, QtWebEngineCore, QtWebEngineWidgets, QtWebChannel
from .tracer import trace


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


class QGoogleMap(QtWebEngineWidgets.QWebEngineView) :

	#@trace
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
		self.channel = QtWebChannel.QWebChannel(self)
		self.page().setWebChannel(self.channel)
		self.channel.registerObject('qtWidget', self)

		htmlfile = Path(__file__).parent.absolute() / 'qgmap.html'
		self.load(QtCore.QUrl(htmlfile.as_uri()))


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
		#print(script)
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
		if 'icon' in extra and type(extra['icon']) == str:
			extra = dict(extra, icon = dict(
				iconUrl=extra['icon'],
				iconAnchor=[16, 32],
			))
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


# vim: set ts=4 sw=4 noet
