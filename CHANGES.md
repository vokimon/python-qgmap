# Changelog

## 1.0.1 (2024-11-26)

- Fix: resources were not included in the package
- Fix: change marker options properly in leaflet
- Fix: base64 encoded markers to enable #RRGGBB colors without escaping 
- Marker icon attribute can be just an image url if the image.
  In that case anchor is placed at 16,32 guessing a 32x32 icon.

## 1.0.0 (2024-11-26)

- Migrated to Qt6
- Using Leaflet instead Google Maps API
- Using OpenStreetMap Geolocation instead Google's
- setTileSet to change the tile set
- Added functions to generate custom markers
- Breaking changes
	- Custom marker options are the ones in leaflet
		- https://leafletjs.com/reference.html#marker

## 0.2 (2014-04-19)




