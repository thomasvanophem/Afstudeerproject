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
import crython
from zipfile import ZipFile
from urllib2 import urlopen, URLError, HTTPError

import config
import logger

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
        
        logger.log("ok", zip_file + " successfully unzipped!", time.strftime("%c"))
    except:
        e = sys.exc_info()[0]
        logger.log("error", e, time.strftime("%c"))
    
    logger.log("busy", "Removing " + zip_file, time.strftime("%c"))
    
    try:
        # Delete the zip archive.
        os.remove(zip_file)
        logger.log("ok", zip_file + " successfully removed!", time.strftime("%c"))
    except:
        e = sys.exc_info()[0]
        logger.log("error", e, time.strftime("%c"))
        
def download(source_url):
    """
    Downloads and save the files specified by source_url.
    """

    # Open the url
    try:
        logger.log("busy", "Downloading " + source_url, time.strftime("%c"))
        
        f = urlopen(source_url)
        
        logger.log("ok", "Download successfull!", time.strftime("%c"))
        
        destination_file = "./Download/" + os.path.basename(source_url)
        
        # Open our local file for writing
        with open(destination_file, "wb") as local_file:
            local_file.write(f.read())

    # Handle errors
    except HTTPError, e:
        logger.log("warning", "Download unsuccessfull!", time.strftime("%c"))
        logger.log("error", str(e) + " " + source_url, time.strftime("%c"))
    except URLError, e:
        logger.log("warning", "Download unsuccessfull!", time.strftime("%c"))
        logger.log("error", str(e) + " " + source_url, time.strftime("%c"))

@crython.job(expr='@daily', ctx='process')        
def download_helper():
    """
    Specifies the files to download and calls the download function.
    """
    
    # Check if the Download directory exists.
    if not os.path.isdir("Download"):
        os.makedirs("Download");
        logger.log("info", "Downoad directory created...", time.strftime("%c"))
    
    logger.log("info", "Starting GEO DATA download...", time.strftime("%c"))
    
    # Download all the files in config.download_files.               
    for url in config.download_files:
        download(url)
    
    logger.log("info", "Completed GEO DATA download...", time.strftime("%c"))
    logger.log("info", "Starting GEO DATA unzip...", time.strftime("%c"))
    
    # Unzip all the zip files in the Download directory.
    for f in glob.glob("./Download/*.zip"):
        unzip_file(f)
    
    logger.log("info", "Completed GEO DATA unzip...", time.strftime("%c"))
    
if __name__ == "__main__":
    download_helper()
