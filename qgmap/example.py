#!/usr/bin/env python

from qgmap import QGoogleMap, QtCore, QtWidgets
from qgmap.presets import tilesets, googlePin, customPin

def main():
	def goCoords() :
		def resetError() :
			coordsEdit.setStyleSheet('')
		try : latitude, longitude = coordsEdit.text().split(",")
		except ValueError :
			coordsEdit.setStyleSheet("color: red;")
			QtCore.QTimer.singleShot(500, resetError)
		else :
			gmap.centerAt(latitude, longitude)
			gmap.moveMarker("MyDragableMark", latitude, longitude)

	def goAddress() :
		def resetError() :
			addressEdit.setStyleSheet('')
		coords = gmap.centerAtAddress(addressEdit.text())
		if coords is None :
			addressEdit.setStyleSheet("color: red;")
			QtCore.QTimer.singleShot(500, resetError)
			return
		gmap.moveMarker("MyDragableMark", *coords)
		coordsEdit.setText("{}, {}".format(*coords))

	def onMarkerMoved(key, latitude, longitude) :
		print("Moved!!", key, latitude, longitude)
		coordsEdit.setText("{}, {}".format(latitude, longitude))
	def onMarkerRClick(key) :
		print("RClick on ", key)
		gmap.setMarkerOptions(key, draggable=0)
	def onMarkerLClick(key) :
		print("LClick on ", key)
	def onMarkerDClick(key) :
		print("DClick on ", key)
		gmap.setMarkerOptions(key, draggable=1)

	def onMapMoved(latitude, longitude) :
		print("Moved to ", latitude, longitude)
	def onMapRClick(latitude, longitude) :
		print("RClick on ", latitude, longitude)
	def onMapLClick(latitude, longitude) :
		print("LClick on ", latitude, longitude)
	def onMapDClick(latitude, longitude) :
		print("DClick on ", latitude, longitude)
	def onSetTileSet(tilesetName):
		gmap.setTileSet(
			tilesets.get(tilesetName) or 
			tilesets['osm']
		)

	print("Creatting app")

	app = QtWidgets.QApplication([])
	w = QtWidgets.QDialog()
	h = QtWidgets.QVBoxLayout(w)
	l = QtWidgets.QFormLayout()
	h.addLayout(l)

	addressEdit = QtWidgets.QLineEdit()
	l.addRow('Address:', addressEdit)
	addressEdit.editingFinished.connect(goAddress)
	coordsEdit = QtWidgets.QLineEdit()
	l.addRow('Coords:', coordsEdit)
	coordsEdit.editingFinished.connect(goCoords)
	tilesetSelector = QtWidgets.QComboBox(w)
	tilesetSelector.addItems([
		key for key in tilesets
	])
	l.addRow("Tile set", tilesetSelector)
	tilesetSelector.currentTextChanged.connect(onSetTileSet)

	gmap = QGoogleMap(w)
	gmap.mapMoved.connect(onMapMoved)
	gmap.mapClicked.connect(onMapLClick)
	gmap.mapDoubleClicked.connect(onMapDClick)
	gmap.mapRightClicked.connect(onMapRClick)
	gmap.markerMoved.connect(onMarkerMoved)
	gmap.markerClicked.connect(onMarkerLClick)
	gmap.markerDoubleClicked.connect(onMarkerDClick)
	gmap.markerRightClicked.connect(onMarkerRClick)
	h.addWidget(gmap)
	gmap.setSizePolicy(
		QtWidgets.QSizePolicy.MinimumExpanding,
		QtWidgets.QSizePolicy.MinimumExpanding)
	w.show()

	gmap.waitUntilReady()

	gmap.centerAt(41.35,2.05)
	gmap.setZoom(13)
	coords = gmap.centerAtAddress("Pau Casals 3, Santa Coloma de Cervelló")
	if coords:
		gmap.addMarker("MyDragableMark", *coords, 
			icon=customPin('green'),
			draggable=1,
			title = "Move me!"
		)

	# Some Static points
	for place in [
		"Pau Casals 13, Santa Coloma de Cervelló",
		"Ferrer 20, Santa Coloma de Cervelló",
		"San Joan Despi",
		]:
		gmap.addMarkerAtAddress(place,
			icon=customPin('darkred'),
		)



	app.exec()


if __name__ == '__main__' :
	main()


