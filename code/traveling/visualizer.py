from PIL import Image, ImageDraw, ImageFont
import fileio
import tsp

def makeTour(best, cities):
    
    tour = []
    
    for i in best:
        tour.append(cities[i])
    return tour


def loadTourNum(tour, cities):
    
    tourNum = []
    
    for i in tour:
        tourNum.append(cities.index(i))
        
    return tourNum


def loadTour(tourFile):
    
    f = open(tourFile, "r")
    tour = []
    
    for t in f.readlines():
        b = t.split("\n")[0]
        tour.append(b)
        
    f.close()    
    
    return tour


def loadCityFile(cityFile):
    f = open(cityFile, "r")
    cl = {}
    
    for l in f.readlines():
        b = l.split(":")
        cl[b[0]] = (float(b[1]), float(b[2]))
    
    f.close()
    return cl
    

def makeBGHash(cl, lx = 110, rx = 1377, by = 750, uy = 120):
    """Map gps coordinates to a map.  Coordinates are 
    mapped using lx, rx, by, and uy.  These variables correspond to the 
    left and right most city x values and the top and bottom most city 
    y values as related to the given background image.
    
    cl = cityList
    
    cl is a hash (sorry not a list) of cities as keys and values being 
    a tuple of coordinates (x, y)
    
    returns a hash in modified coordinates.
    """
    maxx = -1000
    maxy = -1000
    minx = 1000
    miny = 1000
    
    ch = {}
    
    for x,y in cl.values():
        maxx = max(x,maxx)
        maxy = max(y,maxy)
        minx = min(x, minx)
        miny = min(y, miny)
        
    sx = (rx - lx)/((maxx - minx) * 1.0)
    sy = (uy - by)/((maxy - miny) * 1.0)
    
    for c in cl.keys():
        x = cl[c][0]
        y = cl[c][1]
        xc = int((x - minx)*sx + lx)
        yc = int((y - maxy)*sy + uy)
        
        ch[c] = (xc, yc)

    return ch

def plotTour(tour, cityHash, outFile = "./images/best_tour.png", \
            background = "./files/usa.png", lx = 110, \
            rx = 1377, by = 750, uy = 120, es = 5):
        
    img = Image.open(background)
    d = ImageDraw.Draw(img)
    
    plotCities(d, cityHash)
    plotLines(d, tour, cityHash)
    
    del d
    
    img.save(outFile, "PNG")



def plotLines(imd, tour, ch, width = 3):
    
    xOld = None
    yOld = None
    
    first = tour[0]

    for t in tour:
        x = ch[t][0]
        y = ch[t][1]

        if xOld:
            imd.line((xOld, yOld, x, y), fill = (0, 0, 0), width = 4)
    
        xOld = x
        yOld = y

    imd.line((xOld, yOld, ch[first][0], ch[first][1]), fill = (0, 0, 0), \
                width = 4)


def plotCities(imd, ch, s = 5):
    """For a given city hash, draws the points onto a img draw object.
    """

    for x,y in ch.values():
        imd.ellipse((x - s, y - s, x + s, y + s), \
                    fill = (0, 0, 0))


if __name__ == "__main__":
    cl = loadCityFile("./files/cityPixels.txt")
    tour = loadTour("tour.txt")
    cities = fileio.readCities("./files/cities.txt")
    tourNum = loadTourNum(tour, cities)
    dist = fileio.readDistances("./files/distMiles.txt")
    plotTour(tour, cl)
    print "Tour length:" + str(tsp.tour_length(dist,tourNum))
