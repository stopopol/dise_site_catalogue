# Script to harvest EF records from DEIMS-SDR
#
# https://www.deims.org/emf/harvest/json
import csv
import urllib, json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import sys
reload(sys)
sys.setdefaultencoding('utf8')

url="https://www.deims.org/emf/harvest/json"

response = urllib.urlopen(url)
data = json.loads(response.read())
counter = 0

with open('sites.csv', mode='ab') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for x in data['nodes']:
        # limit the amount of processed records
        #counter = counter+1
        #if counter == 50:
        #   break    
        #print(x['node']['deimsid'] + '; ' + x['node']['path'])
        #print x['node']['path']

        response = urllib.urlopen(x['node']['path'])
        e = xml.etree.ElementTree.parse(urllib.urlopen(x['node']['path'])).getroot()
    
        # Site Name
        for name in e.findall("./{http://inspire.ec.europa.eu/schemas/ef/4.0}name"):
            site_name = name.text
        # General Description
        for general_description in e.findall("./{http://inspire.ec.europa.eu/schemas/ef/4.0}additionalDescription"):
            site_description = general_description.text
        # Geometry
        for geometry in e.findall("./{http://inspire.ec.europa.eu/schemas/ef/4.0}geometry"):
            all_descendants = list(geometry.iter())
            for geometry_subelement in all_descendants:
                coords_string = str(geometry_subelement.text)
                if not coords_string.isspace():
                    coordinate_pair = coords_string.split()
                    # filter the complex bounding coordinates
                    if (len(coordinate_pair) == 2):
                        lat = coordinate_pair[0]
                        lon = coordinate_pair[1]
                        wkt_coordinates = "POINT (" + lon + " " + lat + ")"
                        site_writer.writerow([site_name, wkt_coordinates,'deims', site_description])
        

    #{http://inspire.ec.europa.eu/schemas/ef/4.0}responsibleParty"):
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}responsibleParty"):
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}geometry"):
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}onlineResource"):
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}representativePoint
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}measurementRegime
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}mobile
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}operationalActivityPeriod
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}belongsTo
    #{http://inspire.ec.europa.eu/schemas/ef/4.0}belongsTo

