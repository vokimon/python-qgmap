// main var
var map;
var markers=[];
var qtWidget=undefined;

// main init function
function initialize() {
	new QWebChannel(qt.webChannelTransport, function(channel) {
		if (typeof channel.objects != 'undefined') {
			qtWidget = window.qtWidget = channel.objects.qtWidget;
		}
		var myOptions = {
			zoom: 12,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		console.error(google.maps)

		var div = document.getElementById("map_canvas");
		map = new google.maps.Map(div, myOptions);

		google.maps.event.addListener(map, 'dragend', function() {
			center = gmap_getCenter();
			qtWidget.mapMoved(center.lat(), center.lng());
		});
		google.maps.event.addListener(map, 'click', function(ev) {
			qtWidget.mapClicked(ev.latLng.lat(), ev.latLng.lng());
		});
		google.maps.event.addListener(map, 'rightclick', function(ev) {
			qtWidget.mapRightClicked(ev.latLng.lat(), ev.latLng.lng());
		});
		google.maps.event.addListener(map, 'dblclick', function(ev) {
			qtWidget.mapDoubleClicked(ev.latLng.lat(), ev.latLng.lng());
		});
	});
}

// custom functions
function gmap_setCenter(lat, lng)
{
    map.setCenter(new google.maps.LatLng(lat, lng));
}

function gmap_getCenter()
{
	return map.getCenter();
}

function gmap_setZoom(zoom)
{
    map.setZoom(zoom);
}

function gmap_addMarker(key, latitude, longitude, parameters)
{

	if (key in markers) {
		gmap_deleteMarker(key);
	}

	var coords = new google.maps.LatLng(latitude, longitude);
	parameters['map'] = map
	parameters['position'] = coords;

	var marker = new google.maps.Marker(parameters);
	google.maps.event.addListener(marker, 'dragend', function() {
		qtWidget.markerMoved(key, marker.position.lat(), marker.position.lng())
	});
	google.maps.event.addListener(marker, 'click', function() {
		qtWidget.markerClicked(key, marker.position.lat(), marker.position.lng())
	});
	google.maps.event.addListener(marker, 'dblclick', function() {
		qtWidget.markerDoubleClicked(key, marker.position.lat(), marker.position.lng())
	});
	google.maps.event.addListener(marker, 'rightclick', function() {
		qtWidget.markerRightClicked(key, marker.position.lat(), marker.position.lng())
	});

	markers[key] = marker;
	return key;
}

function gmap_moveMarker(key, latitude, longitude)
{
	var coords = new google.maps.LatLng(latitude, longitude);
	markers[key].setPosition(coords);
}

function gmap_deleteMarker(key)
{
	markers[key].setMap(null);
	delete markers[key]
}

function gmap_changeMarker(key, extras)
{
	if (!(key in markers)) {
		return
	}
	markers[key].setOptions(extras);
}


