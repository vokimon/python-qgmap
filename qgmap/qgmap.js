// global vars

var map;
var markers=[];
var tileset=undefined;
var qtWidget=undefined;

const defaultLocation = [41.368056,2.058056]
const defaultZoom = 16 
const defaultTileSet = {
	urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}

// utilities

function showMethods(object) {
	//console.error(JSON.stringify(object.toJSON()))
	for (method in object) {
		console.error("method", method)
	}
}

function event_latlng(ev) {
	return [ ev.latlng.lat, ev.latlng.lng ]
}

function processMarkerExtras(extras) {
	if (extras && extras['icon']) {
		extras.icon = L.icon(extras.icon)
	}
}



// main init function

function initialize() {
	new QWebChannel(qt.webChannelTransport, function(channel) {
		map = L.map('map').setView(defaultLocation, defaultZoom);

		gmap_setTileSet(defaultTileSet)

		qtWidget = window.qtWidget = channel.objects.qtWidget;

		map.on('moveend', function() {
			qtWidget.emitMapMoved(...gmap_getCenter());
		});
		map.on('click', function(ev) {
			qtWidget.emitMapClicked(...event_latlng(ev));
		});
		map.on('contextmenu', function(ev) {
			qtWidget.emitMapRightClicked(...event_latlng(ev));
		});
		map.on('dblclick', function(ev) {
			qtWidget.emitMapDoubleClicked(...event_latlng(ev));
		});
	});
}

// custom functions

function gmap_setTileSet(params)
{
	const {urlTemplate, ...options} = params
	if (tileset) tileset.remove()
	tileset = L.tileLayer(urlTemplate, options)
	tileset.addTo(map)
}

function gmap_setCenter(lat, lng)
{
	map.panTo([lat, lng]);
}

function gmap_getCenter()
{
	const latlng = map.getCenter()
	return [latlng.lat, latlng.lng]
}

function gmap_setZoom(zoom)
{
	map.setZoom(zoom);
}

function gmap_addMarker(key, latitude, longitude, parameters)
{
	if (markers[key]) {
		gmap_deleteMarker(key);
	}
	processMarkerExtras(parameters)

	var marker = L.marker([latitude, longitude], parameters).addTo(map)

	marker.on('moveend', function() {
		qtWidget.emitMarkerMoved(key, ...gmap_getCenter());
	});
	marker.on('click', function(ev) {
		qtWidget.emitMarkerClicked(key, ...event_latlng(ev));
	});
	marker.on('contextmenu', function(ev) {
		qtWidget.emitMarkerRightClicked(key, ...event_latlng(ev));
	});
	marker.on('dblclick', function(ev) {
		qtWidget.emitMarkerDoubleClicked(key, ...event_latlng(ev));
	});

	markers[key] = marker;
	return key;
}

function gmap_moveMarker(key, latitude, longitude)
{
	if (!(key in markers)) {
		console.error(`Marker ${key} not found`)
		return
	}
	markers[key].setLatLng([latitude, longitude]);
}

function gmap_deleteMarker(key)
{
	if (!markers[key]) {
		console.error(`Marker ${key} not found`)
		return
	}
	markers[key].remove();
	delete markers[key]
}

function gmap_changeMarker(key, extras)
{
	if (!markers[key]) {
		console.error(`Marker ${key} not found`)
		return
	}
	processMarkerExtras(extras)
	L.setOptions(markers[key], extras);
}

window.onload = initialize()

// vim: et ts=2 sw=2 noet
