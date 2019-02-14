import pysolr
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# https://confusedcoders.com/data-engineering/search/solr/indexing-csv-data-in-solr-via-python-pysolr
# http://efimeres.com/2016/02/pysolr-solr/

# Setup a basic Solr instance. The timeout is optional.
solr = pysolr.Solr('http://geograph01.umweltbundesamt.at:8983/solr/sites', timeout=10)

# delete all documents first
solr.delete(q='*:*')

# How you would index data.
#solr.add([  
#    {
#        "id": "test_1",
#        "site_name": "zoebelboden", 
#        "geom": "16,38",
#        "catalogue:": "catalogue",
#        "description": "test record for data ingestion",
#        "country": "Austria",
#    }
#])

with open('sites.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            geom = row[0]
            coords = geom[7:-1].split()
            # catalogue
            try:
                catalogue = str(row[4])
            except:
                print "catalogue couldn't be parsed"
                catalogue = "error"
            try:
                formatted_coords = str(coords[1]) + "," + str(coords[0])
                # filter if geom is not valid
                if str(coords[1]) == "?":
                   continue
                # filter if geom not numeric
                try:
                    float(str(coords[1]))
                except ValueError:
                    formatted_coords = "0,0"
            except IndexError:
                formatted_coords = "0,0"

            try:
                country = str(row[1])
            except IndexError:
                country = "undefined"

            print str(row[2])
            print line_count

            solr.add([  
                {
                    "id": line_count,
                    "site_name": str(row[3]),
                    "geom": formatted_coords,
                    "catalogue": catalogue,
                    "description": str(row[5]),
                    "country": country,
                    "site_url": str(row[2])
                }
            ])


# reload solr core
reload_core = requests.get('http://geograph01.umweltbundesamt.at:8983/solr/admin/cores?action=RELOAD&core=sites')