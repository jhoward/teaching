def readCities(fileName):
    """Open the file containing the city names.
    City names must be of the type <City Name>, <State Name>
    """
    f = open(fileName, "r")
    cities = []
    
    for city in f.readlines():
        tmp = city.split('\n')
        cities.append(tmp[0])
        
    return cities
    
    
def writeDistances(fileName, distances, delim = " "):
    """Write a file denoting the distances between all possible pairings from
    the city list.
    """
    f = open(fileName, "w")

    for i in range(len(distances)):
        for j in range(len(distances[i])):
            f.write(str(distances[i][j]) + delim)
        f.write("\n")
    f.close()


def writeCityCoordinates(fileName, cities, delim = " "):
    f = open(fileName, "w")
    
    for i in range(len(cities)):
        f.write(str(cities[i][0]) + delim + str(cities[i][1]) + \
                    delim + str(cities[i][2]))
        f.write('\n')
    f.close()


def writeTour(fileName, tour):
    f = open(fileName, "w")
    
    for i in tour:
        f.write(str(i) + "\n")
    f.close()

        
def readDistances(fileName):
    """Read the file containt all pairings from the city list.
    """
    
    distances = []
    f = open(fileName, "r")
    
    for line in f.readlines():
        distances.append([])
        tmp = line.split(", ")
        for i in range(len(tmp)):
            try:
                distances[-1].append(float(tmp[i]))
            except:
                break
    return distances
        
        
    