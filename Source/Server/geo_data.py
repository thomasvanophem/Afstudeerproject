"""
Downloads the different files (database dumps) from geonames.org. This way we 
don't have to connect to the geonames databasae for each request but just once a
day to download the files.

Author: Thomas van Ophem, thomas.vanophem@student.uva.nl
Date: 29-04-2014
"""

import os
import time
import glob
import sys
import math
from zipfile import ZipFile
from urllib2 import urlopen, URLError, HTTPError

import config
import logger
import database

def unzip_file(zip_file):
    """
    Unzips the file specified by zip_file and writes the content of files in the 
    archive to disk.
    """
    
    logger.log("busy", "Extracting " + zip_file, time.strftime("%c"))
    
    try:
        # Open to zip archive to read the containing files.
        f = open(zip_file, 'rb')
        zipfile = ZipFile(f)
        
        # Write each file in the archive to disk.
        for name in zipfile.namelist():
            destination_file = open("./Download/" + name, 'wb')
            destination_file.write(zipfile.read(name))
            destination_file.close()
 
        f.close()
        
        logger.log("ok", zip_file + " successfully unzipped", time.strftime("%c"))
    except:
        e = sys.exc_info()[0]
        logger.log("error", str(e), time.strftime("%c"))
    
    logger.log("busy", "Removing " + zip_file, time.strftime("%c"))
    
    try:
        # Delete the zip archive.
        os.remove(zip_file)
        logger.log("ok", zip_file + " successfully removed", time.strftime("%c"))
    except:
        e = sys.exc_info()[0]
        logger.log("error", str(e), time.strftime("%c"))

def write_cities_to_database():
    db = database.Database("geo_data.db")
    db.create_table("cities", ["ID INTEGER PRIMARY KEY ASC", 
                                "NAME TEXT NOT NULL",
                                "POP INT NOT NULL",
                                "LAT REAL NOT NULL",
                                "LON REAL NOT NULL",
                                "COUNTRY_CODE TEXT NOT NULL"])              
    temp = open("./Download/cities1000.txt", 'r')
        
    for line in temp:
        l = line.split("\t")
        
        db.insert("cities", ["NAME", "POP", "LAT", "LON",
                            "COUNTRY_CODE"], 
                            [l[2], int(l[14]), math.radians(float(l[4])), 
                            math.radians(float(l[5])), l[8]])
    
    temp.close()
        
    db.close()

def write_countries_to_database():
    db = database.Database("geo_data.db")
    db.create_table("countries", ["NAME TEXT NOT NULL", "CODE TEXT NOT NULL"])   
    
    temp = open("./Download/countryInfo.txt", 'r')

    for line in temp:
        if line[0] != "#":
            l = line.split("\t")
            db.insert("countries", ["NAME", "CODE"], [l[4], l[0]])

    temp.close()

    db.close()

def download(source_url):
    """
    Downloads and save the files specified by source_url.
    """

    # Open the url
    try:
        logger.log("busy", "Downloading " + source_url, time.strftime("%c"))
        
        f = urlopen(source_url)
        
        logger.log("ok", "Download successful", time.strftime("%c"))
        
        destination_file = "./Download/" + os.path.basename(source_url)
        
        # Open our local file for writing
        with open(destination_file, "wb") as local_file:
            local_file.write(f.read())

    # Handle errors
    except HTTPError as e:
        logger.log("warning", "Download unsuccessful", time.strftime("%c"))
        logger.log("error", str(e) + " " + source_url, time.strftime("%c"))
    except URLError as e:
        logger.log("warning", "Download unsuccessful", time.strftime("%c"))
        logger.log("error", str(e) + " " + source_url, time.strftime("%c"))
       
def download_helper():
    """
    Specifies the files to download and calls the download function.
    """
    
    # Check if the Download directory exists.
    if not os.path.isdir("Download"):
        os.makedirs("Download");
        logger.log("info", "Downoad directory created", time.strftime("%c"))
    
    if config.download:
        db = database.Database("geo_data.db")
        db.drop_table("cities")
        db.drop_table("countries")
        db.close()

        logger.log("info", "Starting GEO DATA download", time.strftime("%c"))
        
        # Download all the files in config.download_files.               
        for url in config.download_files:
            download(url)
        
        logger.log("info", "Completed GEO DATA download", time.strftime("%c"))
        logger.log("info", "Starting GEO DATA unzip", time.strftime("%c"))
        
        
        # Unzip all the zip files in the Download directory.
        for f in glob.glob("./Download/*.zip"):
            unzip_file(f)
        
        logger.log("info", "Completed GEO DATA unzip", time.strftime("%c"))    
        
        write_cities_to_database()
        write_countries_to_database()
    else:
        logger.log("info", "GEO DATA already downloaded", time.strftime("%c"))
    
if __name__ == "__main__":
    download_helper()
