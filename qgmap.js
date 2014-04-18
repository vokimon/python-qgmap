// main var
var map;

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

