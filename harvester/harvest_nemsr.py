# Script to harvest site records from the Australian National Environmental Information Infrastructure
#
# http://www.neii.gov.au/nemsr/using

# https://operations.osmfoundation.org/policies/nominatim/
import urllib, json, csv

list_of_subnetworks = []
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=1")
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=2")
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=3")
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=4")
# ...
list_of_subnetworks.append("http://neii.bom.gov.au/cgi-bin/nemsr/get_geojson.py?network_id=28")

total_count = 0
for url in list_of_subnetworks:

  response = urllib.urlopen(url)
  data = json.loads(response.read())

  counter = 0
  with open('sites.csv', mode='ab') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for x in data['features']:
      counter = counter+1
      site_name = x['properties']['name']
      site_description = x['properties']['siteDescription']
      lat  = x['properties']['latitude']
      lon  = x['properties']['longitude']
      wkt_coordinates = "POINT (" + lon + " " + lat + ")"

      site_id = x['properties']['siteURL']
      
      site_writer.writerow([wkt_coordinates, "Australia", site_id, site_name,'NEMSR', site_description])
  
  total_count = total_count + counter

print "Processed NEMSR records: " + str(total_count)
