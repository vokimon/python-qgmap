// main var
var map;
var markers=[];

// main init function
function initialize() {
    var myOptions = {
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}

// custom functions
function setGMapCenter(lat, lng)
{
    map.setCenter(new google.maps.LatLng(lat, lng));
}

function setGMapZoom(zoom)
{
    map.setZoom(zoom);
}

function addGMapMarker(key, latitude, longitude, parameters)
{

	if (key in markers) {
		deleteMarker(key);
	}

	var coords = new google.maps.LatLng(latitude, longitude);
	parameters['map'] = map
	parameters['position'] = coords;

	var marker = new google.maps.Marker(parameters);
	google.maps.event.addListener(marker, 'dragend', function() {
		qtWidget.markerMoved(key, marker.position.lat(), marker.position.lng())
	});

	markers[key] = marker;
	return key;
}

function moveMarker(key, latitude, longitude)
{
	var coords = new google.maps.LatLng(latitude, longitude);
	markers[key].setPosition(coords);
}

function deleteMarker(key)
{
	markers[key].setMap(null);
	delete markers[key]
}




