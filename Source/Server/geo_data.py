"""
Downloads the different files (database dumps) from geonames.org. This way we 
don't have to connect to the geonames databasae for each request but just once a
day to download the files.

Author: Thomas van Ophem, thomas.vanophem@student.uva.nl
Date: 20-05-2015
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
min_cities = 6
max_cities = 15

def get_cities(db_name, r, lat, lon):
    """
    Returns a list of cities in the area represented by mid point (lat, lon) and
    radius r.

    lat and lon both in degrees.
    r is a float, the radius in km.
    """
    result = []

    # Calculate the minimal and maxiimal latitude and longitude.
    dlon = math.asin(math.sin(r)/math.cos(lat))
    
    lat_min = str(lat - r)
    lat_max = str(lat + r)
    lon_min = str(lon - dlon)
    lon_max = str(lon + dlon)
    
    # Which fields do we want to select from our database?
    fields = ["cities.NAME", "cities.LAT", "cities.LON", "cities.POP", "countries.NAME"]

    # Construct the where clause using the spherical law of cosines and minimal and maximal latitude and longitude.
    where = "cities.COUNTRY_CODE = countries.CODE AND (cities.LAT >= " + lat_min + " AND  cities.LAT <= " + lat_max + \
            ") AND (cities.LON >= " + lon_min + " AND cities.LON <= " + lon_max + ")" + \
            " GROUP BY cities.NAME HAVING acos(sin(" + str(lat) + ") * sin(cities.LAT) + cos(" + \
            str(lat) + ") * cos(cities.LAT) * cos(cities.LON - (" + str(lon) + "))) <= " + str(r) + \
            " AND cities.pop != 0"
    
    # Connect to the database and run the query.
    db = database.Database(db_name)
    
    for row in db.select("cities, countries", fields, where):
        result.append(row)
    
    db.close()
    
    return result

def split_cities(cities):
    """
    Algorithm to get a representation of the area.

    cities is a list of cities.
    """
    result = []
    nw, ne, se, sw = [], [], [], []
    
    if len(cities) > 0:
        # Get the biggest city in the selection and add it to the result set.
        biggest = get_biggest(cities)
        result.append(biggest)
        try:
            cities.remove(biggest)
        except ValueError as e:
            # DEBUG
            print cities
            print biggest

        for city in cities:
            bearing = get_bearing((biggest[1], biggest[2]), (city[1], city[2]))

            if bearing < 90.0:
                ne.append(city)
            elif bearing < 180.0:
                se.append(city)
            elif bearing < 270.0:
                sw.append(city)
            else:
                # 270.0 >= bearing <= 360.0
                nw.append(city)

        if len(nw) < min_cities:
            # less then the minimum, just append the biggest city to the result set.
            result.append(get_biggest(nw))
        else:
            #len(nw) >= 5
            # greater the the minimum, split the list of cities and append the result.
            for city in split_cities(nw):
                result.append(city)

        if len(ne) < min_cities:
            # less then the minimum, just append the biggest city to the result set.
            result.append(get_biggest(ne))
        else:
            #len(nw) >= 5
            # greater the the minimum, split the list of cities and append the result.
            for city in split_cities(ne):
                result.append(city)

        if len(se) < min_cities:
            # less then the minimum, just append the biggest city to the result set.
            result.append(get_biggest(se))
        else:
            #len(nw) >= 5
            # greater the the minimum, split the list of cities and append the result.
            for city in split_cities(se):
                result.append(city)

        if len(sw) < min_cities:
            # less then the minimum, just append the biggest city to the result set.
            result.append(get_biggest(sw))
        else:
            #len(nw) >= 5
            # greater the the minimum, split the list of cities and append the result.
            for city in split_cities(sw):
                result.append(city)

    # Remove the empty tuples from the result set and return the result.
    return [city for city in result if city != ()]

# Returns the bearing from big to city.
def get_bearing(big, city):
    """
    Return the bearing from big to city.
    big = (lat, lon)
    city = (lat, lon)

    lat and lon both in degrees.
    """
    # Convert latitude of both cities to radians.
    lat_big = math.radians(big[0])
    lat_city = math.radians(city[0])

    # Convert the difference in longitude to radians.
    d_lon = math.radians(city[1] - big[1])

    x = math.sin(d_lon) * math.cos(lat_city)
    y = math.cos(lat_big) * math.sin(lat_city) - (math.sin(lat_big) * math.cos(lat_city) * math.cos(d_lon))

    # Convert bearing to degrees.
    bearing = math.degrees(math.atan2(x, y))

    # Make sure it is a number between 0.0 and 360.0.
    temp = (bearing + 360) % 360

    return temp

def get_biggest(cities):
    """
    Returns the biggest city in the list cities.
    The fourth element of each sublist in cities is the population.
    """
    t = 0
    result = ()

    for city in cities:
        if city[3] > t:
            t = city[3]
            result = city
            
    return result
    
def main(db, source, radius):
    r = float(radius) / 6371
    lat = math.radians(float(source[0]))
    lon = math.radians(float(source[1]))
    cities = get_cities(db, r, lat, lon)

    # If the number of cities in the area is more than the maximum we have to 
    # run the algorithm for area representation.
    if len(cities) > max_cities:
        temp = cities[:]
        
        while len(temp) > max_cities:
            temp = split_cities(temp)
            
        result = temp[:]

        num_cities = len(result)

        while num_cities < max_cities:
            for city in result:
                try:
                    cities.remove(city)
                except:
                    pass
            temp2 = cities[:]
            
            if config.debug == True:
                print "# results: ", len(result), "# temp2: ",  len(temp2), "# diff: ", max_cities - num_cities

            if (max_cities - num_cities) == 1:
                result.append(get_biggest(temp2))
            elif len(temp2) < (max_cities - num_cities):
                result += temp2
            elif (max_cities - num_cities) < 5:
                for i in range((max_cities - num_cities)):
                    biggest = get_biggest(temp2)
                    temp2.remove(biggest)
                    result.append(biggest)
            else:
                while len(temp2) > (max_cities - num_cities):
                    temp2 = split_cities(temp2)

                result += temp2

            num_cities = len(result)      
    else:
        result = cities[:]
    
    if config.debug == True:    
        print "# cities: ", len(cities)
        print "# result: ", len(result)
    
    return result

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

    t = main("geo_data.db", (52.6333333, 4.75), 50)
    print t
