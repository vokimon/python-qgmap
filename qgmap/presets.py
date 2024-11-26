import base64

# https://leaflet-extras.github.io/leaflet-providers/preview/
tilesets = dict(
	osm = dict(
		urlTemplate = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
		attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	),
	google_satellite = dict(
		urlTemplate = 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
		maxZoom = 20,
		subdomains = ['mt0','mt1','mt2','mt3'],
	),
	google_hibrid = dict(
		urlTemplate = 'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
		maxZoom = 20,
		subdomains =['mt0','mt1','mt2','mt3']
	),
	google_streets = dict(
		urlTemplate = 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
		maxZoom = 20,
		subdomains =['mt0','mt1','mt2','mt3']
	),
	google_terrain = dict(
		urlTemplate = 'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
		maxZoom = 20,
		subdomains =['mt0','mt1','mt2','mt3']
	),
)

def base64DataUrl(content):
	return 'data:image/svg+xml;base64,'+base64.b64encode(content.encode('utf8')).decode('utf8')


def customPin(color):
	path = "M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z M -2,-30 a 2,2 0 1,1 4,0 2,2 0 1,1 -4,0"
	svg = (
		'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="42" viewBox="-12 -42 24 42">' 
		f'<path d="{path}" fill="{color}" stroke="#000000" stroke-width="1"/>'
		'</svg>'
	)
	url = base64DataUrl(svg)
	return dict(
		iconUrl=url,
		iconAnchor=[12,42],
	)

def googlePin(color):
	# Many icons at: https://sites.google.com/site/gmapsdevelopment/
	url = f'http://maps.google.com/mapfiles/ms/micons/{color}-dot.png'
	return dict(
		iconUrl=url,
		iconAnchor=[16, 32],
	)

