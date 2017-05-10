import random
import sa
import fileio
import getopt
import visualizer

max_iterations = 10000

def makeTour(best, cities):
    
    tour = []
    
    for i in best:
        tour.append(cities[i])
    return tour

def rand_seq(size):
    '''generates values in random order
    equivalent to using shuffle in random,
    without generating all values at once'''
    values=range(size)
    for i in xrange(size):
        # pick a random index into remaining values
        j=i+int(random.random()*(size-i))
        # swap the values
        values[j],values[i]=values[i],values[j]
        # return the swapped value
        yield values[i]

def all_pairs(size):
    '''generates all i,j pairs for i,j from 0-size'''
    for i in rand_seq(size):
        for j in rand_seq(size):
            yield (i,j)

def tour_length(matrix,tour):
    '''total up the total length of the tour based on the distance matrix'''
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=matrix[city_i][city_j]
        
    total += matrix[tour[-1]][tour[0]]    
    return total

def init_random_tour(tour_length):
   tour=range(tour_length)
   random.shuffle(tour)
   return tour
   
def reversed_sections(tour):
   '''generator to return all possible variations where the section \
        between two cities are swapped'''
   for i,j in all_pairs(len(tour)):
       if i != j:
           copy=tour[:]
           if i < j:
               copy[i:j+1]=reversed(tour[i:j+1])
           else:
               copy[i+1:]=reversed(tour[:j])
               copy[:j]=reversed(tour[i+1:])
           if copy != tour: # no point returning the same tour
               yield copy
               

def run_sa(iterations, dist, start, alpha, draw = True, every = 100):
    init_function = lambda: init_random_tour(len(dist[0]))
    objective_function = lambda tour: -tour_length(dist, tour)
    move_operator = reversed_sections
    
    iterations,score,best = sa.anneal(init_function, move_operator, \
                                        objective_function, iterations, \
                                        start, alpha, draw, every)
                                        
    print iterations, score, best
    return best


if __name__ == "__main__":
    cities = fileio.readCities("./files/cities.txt")
    dist = fileio.readDistances("./files/distMiles.txt")
    best = run_sa(5000, dist, 100, 0.90, draw=True, every=100)
    
    bt = visualizer.makeTour(best, cities)
    fileio.writeTour("tour.txt", bt)
    
