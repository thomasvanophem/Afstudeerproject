"""
Author: Thomas van Ophem thomas.vanophem@student.uva.nl
Date: 30-04-2014
"""

import math
import glob
import time

import database

min_cities = 6
max_cities = 20
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
            str(lat) + ") * cos(cities.LAT) * cos(cities.LON - (" + str(lon) + "))) <= " + str(r) + \
            " AND cities.pop != 0"
    
    db = database.Database(db_name)
    
    for row in db.select("cities, countries", fields, where):
        result.append(row)
    
    db.close()
    
    return result 
# Returns all the cities which are to the north.
def get_north(start, cities):
    result = []

    for city in cities:
        bearing = get_bearing((start[1], start[2]), (city[1], city[2]))

        if bearing > 270.0 or bearing < 90.0:
            result.append(city)

    return result

# Returns all the city which are to the east.
def get_east(start, cities):
    result = []

    for city in cities:
        bearing = get_bearing((start[1], start[2]), (city[1], city[2]))

        if bearing < 180.0:
            result.append(city)

    return result

def split1(cities):
    result, north, south = [], [], []

    if len(cities) > 0:
        biggest = get_biggest(cities)
        result.append(biggest)

        try:
            cities.remove(biggest)
        except ValueError as e:
            print biggest
            print cities
        
        north = get_north(biggest, cities)

        result += split2(north)

        south = [city for city in cities if city not in north]

        result += split2(south)

    # Remove the empty tuples from the result set and return the result.
    return [city for city in result if city != ()]

def split2(cities):
    result, east, west = [], [], []

    biggest = get_biggest(cities)
    result.append(biggest)

    try:
        cities.remove(biggest)
    except ValueError as e:
        print biggest
        print cities

    east = get_east(biggest, east)

    result += split3(east)

    west = [city for city in cities if city not in east]

    result += split3(west)

    return result

def split3(cities):
    result, north, south = [], [], []

    biggest = get_biggest(cities)
    result.append(biggest)

    try:
        cities.remove(biggest)
    except ValueError as e:
        print biggest
        print cities

    north = get_north(biggest, cities)

    result += split4(north)

    south = [city for city in cities if city not in north]

    result += split4(south)

    return result

def split4(cities):
    result, east, west = [], [], []

    biggest = get_biggest(cities)
    result.append(biggest)

    try:
        cities.remove(biggest)
    except ValueError as e:
        print biggest
        print cities

    east = get_east(biggest, cities)
    
    result.append(get_biggest(east))

    west = [city for city in cities if city not in west]

    result.append(get_biggest(west))

    return result

def split_cities(cities):
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
    
    result = split1(cities[:])
    """
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
            
            print len(result), len(temp2), max_cities - num_cities

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
        """
    print len(result)

    return result
    
if __name__ == "__main__":
    t = main("geo_data.db", (52.6333333, 4.75), 50)
    print t
