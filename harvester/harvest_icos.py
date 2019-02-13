# Script to harvest site records from ICOS
#
# https://meta.icos-cp.eu/sparqlclient/?type=CSV
# https://www.icos-cp.eu/stations
import urllib, json, sparql, csv, time
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
# sparql-client has to be installed

# necessary for parsing the special characters in the sparql response
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# https://meta.icos-cp.eu/sparqlclient/?q=Table%20of%20stations&type=JSON
# https://operations.osmfoundation.org/policies/nominatim/
endpoint="https://meta.icos-cp.eu/sparqlclient"
s = sparql.Service(endpoint, "utf-8", "GET")

statement = """PREFIX cpst: <http://meta.icos-cp.eu/ontologies/stationentry/>
                SELECT 
				?s
                (IF(bound(?lat), str(?lat), "?") AS ?latstr)
                (IF(bound(?lon), str(?lon), "?") AS ?lonstr)
                (REPLACE(str(?class),"http://meta.icos-cp.eu/ontologies/stationentry/", "") AS ?themeShort)
                (str(?country) AS ?Country)
                (str(?sName) AS ?Short_name)
                (str(?lName) AS ?Long_name)
                (str(?url) AS ?site_url)
                (GROUP_CONCAT(?piLname; separator=";") AS ?PI_names)
                (str(?siteType) AS ?Site_type)
                FROM <http://meta.icos-cp.eu/resources/stationentry/>
                WHERE {
                ?s cpst:hasCountry ?country .
                ?s cpst:hasShortName ?sName .
                ?s cpst:hasLongName ?lName .
                ?s cpst:hasSiteType ?siteType .
                ?s cpst:hasPi ?pi .
                ?pi cpst:hasLastName ?piLname .
                ?s a ?class .
                OPTIONAL{?s cpst:hasLat ?lat } .
                OPTIONAL{?s cpst:hasLon ?lon } .
                OPTIONAL{?s cpst:hasSpatialReference ?spatRef } .
                OPTIONAL{?pi cpst:hasFirstName ?piFname } .
                }
                GROUP BY ?s ?lat ?lon ?class ?country ?sName ?lName ?siteType ?url
                ORDER BY ?themeShort ?sName
            """
counter = 0
result = s.query(statement)
with open('sites.csv', mode='ab') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for row in result.fetchone():
        counter = counter+1
        site_id = str(row[0])
        site_name = str(row[6])
        site_description = str(row[8])
        lat = str(row[1])
        lon = str(row[2])
        wkt_coordinates = "POINT (" + lon + " " + lat + ")"

        ready_coords = [lat, lon]
        try:
            #country = "Carbon-Phantasia"
            location = geolocator.reverse(ready_coords, language='en', timeout=5)
            country = location.raw['address']['country']
        except GeocoderTimedOut as e:
            country = "timeout"
        site_writer.writerow([wkt_coordinates, country, site_id, site_name,'ICOS', site_description])
        time.sleep(2)

print "Processed ICOS records: " + str(counter)
