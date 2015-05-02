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
    
    fields = ["NAME", "LAT", "LON", "POP"]
    where = "(LAT >= " + lat_min + " AND  LAT <= " + lat_max + \
            ") AND (LON >= " + lon_min + " AND LON <= " + lon_max + ")" + \
            " GROUP BY NAME HAVING acos(sin(" + str(lat) + ") * sin(LAT) + cos(" + \
            str(lat) + ") * cos(LAT) * cos(LON - (" + str(lon) + "))) <= " + str(r)
    
    db = database.Database(db_name)
    
    for row in db.select("cities", fields, where):
        result.append(row)
    
    db.close()
    
    return result    
    
def main(db, source, radius):
    r = float(radius) / 6371
    lat = math.radians(float(source[0]))
    lon = math.radians(float(source[1]))
    cities = get_cities(db, r, lat, lon)
        
    return cities
    
if __name__ == "__main__":
    t = main("geo_data.db", (52.6333333, 4.75), 50)
    print t