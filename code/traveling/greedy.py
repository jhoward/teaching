def greed(startCity, dist, cities):
    
    tour = []
    tour.append(cities.index(startCity))
    
    while tour < len(dist):
        
        #make a new list
        nl = [d for j in range(len(dist[tour[-1]]))]
        nl.sort()
        
        #loop through nl items and find the first not in tour
        for i in nl:
            try:
                a = tour.index(i)
                continue
            except:
                #tour.append(dist[