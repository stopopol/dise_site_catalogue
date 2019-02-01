# Script to harvest site records from the Australian National Environmental Information Infrastructure
#
# http://www.neii.gov.au/nemsr/using

import urllib, json, csv

list_of_subnetworks = []
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=1")
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=2")
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=3")
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=4")
# ...
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=28")

for url in list_of_subnetworks:

  response = urllib.urlopen(url)
  data = json.loads(response.read())

  
  with open('sites.csv', mode='ab') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for x in data['features']:
      site_name = x['properties']['name']
      site_description = x['properties']['siteDescription']
      lat  = x['properties']['latitude']
      lon  = x['properties']['longitude']
      wkt_coordinates = "POINT (" + lon + " " + lat + ")"
      
      site_writer.writerow([site_name, site_description, wkt_coordinates,'nemsr'])
