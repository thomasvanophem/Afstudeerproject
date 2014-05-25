"""
Author: Thomas van Ophem thomas.vanophem@student.uva.nl
Date: 30-04-2014
"""

import math
import glob

def read_file(file_name):
    """
    Reads the contents of a file specified by file_name line by line and returns
    a list of coordinates.
    """
    
    result = []
        
    with open(file_name, "r") as f:
        for line in f:
            result.append((line.split("\t")[2], (line.split("\t")[4], line.split("\t")[5])))
         
    return result
    
    
def calc_distance(source, destination):
    """
    Calculates the distance between two points specified by the tuples of 
    coordinates in source and destination. This uses the Haversine formula.
    For more info see: http://en.wikipedia.org/wiki/Haversine_formula
    """
    
    R = 6371 # Earth radius in KM
    dlat = math.radians(float(destination[0]) - float(source[0]))
    dlon = math.radians(float(destination[1]) - float(source[1]))
    lat1 = math.radians(float(source[0]))
    lat2 = math.radians(float(destination[0]))
    
    a = (math.sin(dlat / 2) * math.sin(dlat / 2)) + \
        (math.sin(dlon / 2) * math.sin(dlon / 2)) * \
        math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c
    
    
def main(source, radius, db, result):
    coordinates = []
    
    coordinates = coordinates + read_file(db)

    for coordinate in coordinates:
        if calc_distance(source, coordinate[1]) <= float(radius) and coordinate[0] not in result:
            result.append(coordinate[0])
    
    if len(result) < 50 and db == "../Download/cities15000.txt":
        main(source, radius, "./Download/cities5000.txt", result)
    elif len(result) < 50 and db == "./Download/cities5000.txt":
        main(source, radius, "./Download/cities1000.txt", result)
    
    return result
