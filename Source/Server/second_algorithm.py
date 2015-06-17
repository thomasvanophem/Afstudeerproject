# SECOND ALGORITHM FOR THE AREA REPRESENTATION, NOT USED!!!!!

# Returns all the cities which are to the north.
def split_north(cities):
    result = []
    big = get_biggest(cities)
    
    try:
        cities.remove(big)
    except ValueError as e:
        print big
        print cities
        
    for city in cities:
        bearing = get_bearing((big[1], big[2]), (city[1], city[2]))

        if bearing > 270.0 or bearing < 90.0:
            result.append(city)

    return big, result, [city for city in cities if city not in result]

# Returns all the city which are to the east.
def split_east(cities):
    result = []
    big = get_biggest(cities)
    print "SOUTH"
    try:
        cities.remove(big)
    except ValueError as e:
        print big
        print cities
        
    for city in cities:
        bearing = get_bearing((big[1], big[2]), (city[1], city[2]))

        if bearing < 180.0:
            result.append(city)

    return big, result, [city for city in cities if city not in result]

def split1(cities):
    result = []

    t = [cities]
    d = 0 # 0 = north/south, not 0 = east/west
    
    while len(result) < max_cities:
        rng = len(t)
        for i in range(rng):
            if d == 0:
                big, north, south = split_north(t[i])
                result.append(big)
                t.append(north[:])
                t.append(south[:])
                t.remove(t[i])
                if i == (rng - 1):
                    d = 1
            else:
                big, east, west = split_east(t[i])
                result.append(big)
                t.append(east[:])
                t.append(west[:])
                t.remove(t[i])

                if i == (rng - 1):
                    d = 0

    return result
	
if __name__ == "__main__":
	# cities is a list of cities return by the sql query.
    # For the second algorithm
    if len(cities) > max_cities:
        result = split1(cities[:])
    else:
        result = cities[:]
		
	For the second algorithm
    if len(result) > max_cities:
        result = result[:max_cities]