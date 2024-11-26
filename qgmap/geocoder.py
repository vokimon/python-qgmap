import json
from .qt import QtNetwork, QtCore, QtWidgets
from .tracer import trace

class GeoCoder(QtNetwork.QNetworkAccessManager) :
	class NotFoundError(Exception) : pass

	#@trace
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


