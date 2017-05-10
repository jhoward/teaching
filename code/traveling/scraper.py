"""
scraper.py
Author: James Howard


Scrapes all cities as drawn from cities.txt

Constructs a distances.txt file which contains the driving distance
between all cities as drawn from cities.txt
"""

import googlemaps
from googlemaps import GoogleMaps
import fileio

def getDistance(gmaps, cityOne, cityTwo):
    results = gmaps.directions(cityOne, cityTwo)
    return results['Directions']['Distance']['meters']


def createCityCoordinateList(gmaps, cityList):
    """Create a list of cities and gps coordinates."""
    cities = []
    print "Calculating gps coordinates."""
    for i in range(len(cityList)):
        r = gmaps.geocode(cityList[i])
        c = r['Placemark'][0]['Point']['coordinates'][0:2]
        cities.append((cityList[i], c[0], c[1]))
        
    return cities


def createDistanceList(gmaps, cityList, convert = 1):
    """Put delimter between each item and divide the value by convert."""
    #First create a list
    distances = []
    print "Cities Calculated:"
    for i in range(len(cityList)):
        distances.append([])
        for j in range(len(cityList)):
            d = getDistance(gmaps, cityList[i], cityList[j])
            distances[i].append(d/(convert * 1.0))
            
        print cities[i]
            
    return distances


if __name__ == "__main__":
    #This may need to be changed if google changes their key policy
    gmaps = GoogleMaps("")
    
    cities = fileio.readCities("./files/cities.txt")
    
    distances = createDistanceList(gmaps, cities, convert=1609.344)
    fileio.writeDistances("distMiles.txt", distances, ", ")
    coord = createCityCoordinateList(gmaps, cities)
    fileio.writeCityCoordinates("./files/5hourclas.txt", coord, ":")
    print "Completed"

