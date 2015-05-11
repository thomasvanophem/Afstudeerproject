"""
Author: Thomas van Ophem thomas.vanophem@student.uva.nl
Date: 30-04-2014
"""

import math
import glob
import time

import database

min_cities = 6
max_cities = 15
def get_cities(db_name, r, lat, lon):
    result = []
    dlon = math.asin(math.sin(r)/math.cos(lat))
    
    lat_min = str(lat - r)
    lat_max = str(lat + r)
    lon_min = str(lon - dlon)
    lon_max = str(lon + dlon)
    
    fields = ["cities.NAME", "cities.LAT", "cities.LON", "cities.POP", "countries.NAME"]
    where = "cities.COUNTRY_CODE = countries.CODE AND (cities.LAT >= " + lat_min + " AND  cities.LAT <= " + lat_max + \
            ") AND (cities.LON >= " + lon_min + " AND cities.LON <= " + lon_max + ")" + \
            " GROUP BY cities.NAME HAVING acos(sin(" + str(lat) + ") * sin(cities.LAT) + cos(" + \
            str(lat) + ") * cos(cities.LAT) * cos(cities.LON - (" + str(lon) + "))) <= " + str(r)
    
    db = database.Database(db_name)
    
    for row in db.select("cities, countries", fields, where):
        result.append(row)
    
    db.close()
    
    return result 

def split_cities(cities):
    result = []
    nw, ne, se, sw = [], [], [], []
    
    if len(cities) > 0:
        # Get the biggest city in the selection and add it to the result set.
        biggest = get_biggest(cities)
        result.append(biggest)
        cities.remove(biggest)

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
"""
def split_cities(cities):
    result = []
    nw, sw, ne, se = [], [], [], []
    
    big = get_biggest(cities)
    
    result.append(big)
    
    cities.remove(big)
    
    for city in (cities):
        t = get_bearing((big[1], big[2]), (city[1], city[2]))
        
        if t < 90.0:
            ne.append(city)
        elif t < 180.0:
            se.append(city)
        elif t < 270.0:
            sw.append(city)
        else:
            nw.append(city)
   
    if len(nw) <= min_cities:
        result.append(get_biggest(nw))
    else:
        for city in split_cities(nw):
            result.append(city)
        
    if len(sw) <= min_cities:
        result.append(get_biggest(sw))
    else:
        for city in split_cities(sw):
            result.append(city)
        
    if len(ne) <= min_cities:
        result.append(get_biggest(ne))
    else:
        for city in split_cities(ne):
            result.append(city)
        
    if len(se) <= min_cities:
        result.append(get_biggest(se))
    else:
        for city in split_cities(se):
            result.append(city)
    
    # Remove empty tuples and return the result
    return [i for i in result if i != ()]"""
    
def get_bearing(big, city): 
    lat_big = math.radians(big[0])
    lat_city = math.radians(city[0])
 
    d_lon = math.radians(city[1] - big[1])
 
    x = math.sin(d_lon) * math.cos(lat_city)
    y = math.cos(lat_big) * math.sin(lat_city) - (math.sin(lat_big) * math.cos(lat_city) * math.cos(d_lon))
 
    bearing = math.degrees(math.atan2(x, y))
    
    temp = (bearing + 360) % 360
 
    return temp
    
def get_biggest(cities):
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
    
    temp = cities[:]
    print len(temp)
    while len(temp) > max_cities:
        temp = split_cities(temp)
        print len(temp)
        print temp

    print len(cities)
    print len(temp)
        
    return temp
    
if __name__ == "__main__":
    t = main("geo_data.db", (52.6333333, 4.75), 50)
    print t
