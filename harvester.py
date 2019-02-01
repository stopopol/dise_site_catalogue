import os
import csv
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#reset csv here
with open('sites.csv', mode='wb') as sites_file:
    site_writer = csv.writer(sites_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    site_writer.writerow(["site_name", "site_description", "geom",'ri'])

deims_path = os.path.dirname(os.path.abspath(__file__)) + "\harvester\harvest_deims.py"
icos_path = os.path.dirname(os.path.abspath(__file__))  + "\harvester\harvest_icos.py"
nemsr_path = os.path.dirname(os.path.abspath(__file__)) + "\harvester\harvest_nemsr.py"

subprocess.Popen(deims_path, shell=True)
subprocess.Popen(icos_path, shell=True)
subprocess.Popen(nemsr_path, shell=True)
