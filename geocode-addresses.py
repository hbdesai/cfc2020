import sys
import xml.etree.ElementTree as ET
import googlemaps
import time
# import json

gmaps = googlemaps.Client(key='AIzaSyBMtSTsV1u6JyhlcQwYrF-E0ZhaEAbC4CU');

# tree = ET.parse('SearchResults.xml')
inputAddressDataFile = sys.argv[1]
outputGeocodedDataFile = sys.argv[2]
log = sys.argv[3]

latd = {}
lngd = {}
gc_updated = 0

## Load known geo locations for lookup
gc_locs_tree = ET.parse('GeocodedLocations.xml')
gc_root = gc_locs_tree.getroot()
# add to existing locations subelement
gc_locs_elem = gc_root[0]
# add to new locations subelement
# gc_locs_elem = ET.SubElement(gc_root, 'locations')

# Cache the known geolocations
for gc_elem in gc_root.iter('location'):
    gc_adr=gc_elem.text
    gc_lat=gc_elem.get('lat')
    if not gc_lat :
        gc_lat='na'
		
    gc_lng=gc_elem.get('lng')
    if not gc_lng :
        gc_lng='na'
		
    latd[gc_adr]=gc_lat
    lngd[gc_adr]=gc_lng

print ('lat: ' + str(len(latd)))
print ('lng: ' + str(len(lngd)))

tree = ET.parse(inputAddressDataFile)
root = tree.getroot()

# changing a field text
i=0
for elem in root.iter('location'):
    address=elem.text
    # is the address not geocoded?
    lat = latd.get(address)
    if not lat : # new address to geocode
        # to store in geolocations
        wLocItem = ET.SubElement(gc_locs_elem, 'location')
        wLocItem.text = address
        gc_updated = 1
		
		# preload the cache with 'na' if can't geocode
        latd[address]='na'
        lngd[address]='na' 
		
        time.sleep(1)
        res = gmaps.geocode(address)
        if len(res) == 0 :  # failed geocode
            if log == 't' :
                print(str(i)+ ". - "+address)
            continue

        if i == -1:
            print(res[0])

        lat = res[0]['geometry']['location']['lat']
        lng = res[0]['geometry']['location']['lng']
        elem.set('lat', str(lat))
        elem.set('lng', str(lng))
		
        # update the attributes to update
        wLocItem.set('lat', str(lat))
        wLocItem.set('lng', str(lng))

        if ( i % 100 == 0) :
            print(str(i) + ' - Updating GeoLocations')
            gc_locs_tree.write('GeocodedLocation-updated.xml')
		
        # update the cache
        latd[address]=lat
        lngd[address]=lng        

    elif lat != 'na' : # found in cache
        lng = lngd[address]

        # set the attributes for the output
        elem.set('lat', lat)
        elem.set('lng', lng)

    i=i+1

if gc_updated == 1 :
    print('Updating GeoLocations')
    gc_locs_tree.write('GeocodedLocation-updated.xml')

tree.write(outputGeocodedDataFile)

