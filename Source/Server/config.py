"""
Config file for the server and download script.

Author: Thomas van Ophem, thomas.vanophem@student.uva.nl
Date: 29-04-2015
"""

# Files to download from the geonames database (database dumps).
download_files = ["http://download.geonames.org/export/dump/cities1000.zip",
                    "http://download.geonames.org/export/dump/countryInfo.txt"]
                    
# Color codes to print fancy info/warning/error messages.     
colors = {'BUSY' : '\033[1;47m', 'INFO' : '\033[1;46m', 'OK' : '\033[1;42m', 
            'WARNING' : '\033[1;43m', 'ERROR' : '\033[1;41m', 
            'END' : '\033[1;m'}
            
log = True
to_file = False
download = False
debug = True
