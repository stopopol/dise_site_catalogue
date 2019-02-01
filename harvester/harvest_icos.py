# Script to harvest site records from ICOS
#
# https://meta.icos-cp.eu/sparqlclient/?type=CSV

import urllib, json, sparql, csv
# sparql-client has to be installed

# necessary for parsing the special characters in the sparql response
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# https://meta.icos-cp.eu/sparqlclient/?q=Table%20of%20stations&type=JSON

endpoint="https://meta.icos-cp.eu/sparqlclient"
s = sparql.Service(endpoint, "utf-8", "GET")

statement = """PREFIX cpst: <http://meta.icos-cp.eu/ontologies/stationentry/>
                SELECT
                (IF(bound(?lat), str(?lat), "?") AS ?latstr)
                (IF(bound(?lon), str(?lon), "?") AS ?lonstr)
                (REPLACE(str(?class),"http://meta.icos-cp.eu/ontologies/stationentry/", "") AS ?themeShort)
                (str(?country) AS ?Country)
                (str(?sName) AS ?Short_name)
                (str(?lName) AS ?Long_name)
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
                GROUP BY ?lat ?lon ?class ?country ?sName ?lName ?siteType
                ORDER BY ?themeShort ?sName

            """

result = s.query(statement)
with open('sites.csv', mode='ab') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in result.fetchone():
        site_name = str(row[5])
        site_description = str(row[7])
        lat = str(row[0])
        lon = str(row[1])
        wkt_coordinates = "POINT (" + lon + " " + lat + ")"
        # <class 'sparql.Literal'>

        site_writer.writerow([site_name, site_description, wkt_coordinates,'icos'])
