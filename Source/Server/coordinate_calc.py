"""
Author: Thomas van Ophem thomas.vanophem@student.uva.nl
Date: 30-04-2014
"""

import math
import glob
import time

import database

def get_cities(db_name, r, lat, lon):
    result = []
    dlon = math.asin(math.sin(r)/math.cos(lat))
    
    lat_min = str(lat - r)
    lat_max = str(lat + r)
    lon_min = str(lon - dlon)
    lon_max = str(lon + dlon)
    
    fields = ["NAME"]
    where = "(LAT >= " + lat_min + " AND  LAT <= " + lat_max + \
            ") AND (LON >= " + lon_min + " AND LON <= " + lon_max + ")" + \
            " GROUP BY NAME HAVING acos(sin(" + str(lat) + ") * sin(LAT) + cos(" + \
            str(lat) + ") * cos(LAT) * cos(LON - (" + str(lon) + "))) <= " + str(r)
    
    db = database.Database(db_name)
    
    for row in db.select("cities", fields, where):
        result.append(row)
    
    db.close()
    
    return result    
    
def cache(db_name, lat, lon, radius, cities):
    db = database.Database(db_name)
    db.create_table("geo_cache", ["ID INTEGER PRIMARY KEY ASC", 
                                    "LAT REAL", "LON REAL", 
                                    "RADIUS REAL", "CITIES TEXT", 
                                    "DATE INTEGER"])
    db.insert("geo_cache", ["LAT", "LON", "RADIUS", "CITIES", "DATE"], 
                            [lat, lon, radius, str(cities), int(time.time())])
    db.close()

def main(db, source, radius):
    r = float(radius) / 6371
    lat = math.radians(float(source[0]))
    lon = math.radians(float(source[1]))
    cities = get_cities(db, r, lat, lon)
    cache("geo_data.db", lat, lon, float(radius), cities)
    
    return cities
    
if __name__ == "__main__":
    main("geo_data.db", (52.6333333, 4.75), 50)
