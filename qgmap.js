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

function addGMapMarker(key, latitude, longitude, draggable)
{
	var myLatlng = new google.maps.LatLng(latitude, longitude);
	var marker = new google.maps.Marker({
		map: map,
		position: myLatlng,
		title: key,
		draggable:draggable,
	});
	google.maps.event.addListener(marker, 'dragend', function() {
		qtWidget.markerMoved(key, marker.position.lat(), marker.position.lng())
	});

	markers[key] = marker;
}



