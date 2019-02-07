import pysolr
import csv

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
#        "description": "test record for data ingestion",
#        "catalogue:": "catalogue",
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
            geom = row[1]
            coords = geom[7:-1].split()
            # catalogue
            print str(row[2])
            try:
                formatted_coords = str(coords[1]) + "," + str(coords[0])
                if str(coords[1]) == "?":
                   continue 
                try:
                    float(str(coords[1]))
                except ValueError:
                    continue
            except IndexError:
                formatted_coords = "0,0"

            print line_count
            solr.add([  
                {
                    "id": line_count,
                    "site_name": str(row[0]),
                    "geom": formatted_coords,
                    "catalogue": str(row[2]),
                    "description": str(row[3]),
                }
            ])