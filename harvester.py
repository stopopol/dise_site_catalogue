import os
import csv
import subprocess
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# write one big csv including site information from all catalogues
# reset csv here
with open('sites.csv', mode='wb') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    site_writer.writerow(["WKT", "country", "id", "site_name", 'catalogue', "site_description"])

deims_path = os.path.dirname(os.path.abspath(__file__)) + "\harvester\harvest_deims.py"
icos_path = os.path.dirname(os.path.abspath(__file__))  + "\harvester\harvest_icos.py"
nemsr_path = os.path.dirname(os.path.abspath(__file__)) + "\harvester\harvest_nemsr.py"

# communicate is necessary, otherwise the subprocesses run in parallel and the csv will be flawed
subprocess.Popen(nemsr_path, shell=True).communicate() 
subprocess.Popen(deims_path, shell=True).communicate() 
subprocess.Popen(icos_path, shell=True).communicate() 

