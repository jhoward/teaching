"""
optimizer.py
Author: James Howard

Performs some basic traveling salesman approaches on dataset given by us 
city distances.

returns a list of city numbers in travel order.
"""

import fileio
import random



def normalizeList(scores):
    """Return a normalized list that adds to one
    
    I should make this whole normalizedList a class so that I can also 
    have a sample method and just draw from the class but I don't really
    feel like that for now.
    """
    sumPop = sum(scores)*1.0
    total = 0
    nl = []
    
    for s in scores:
        total += s/sumPop
        nl.append(total)
        
    return nl

def getParent(nl):
    """NL is a summed normalized list of the type given by the function
    normalizeList above"""
    val = random.random()
    
    for i in range(len(nl)):
        if val < nl[i]:
            return i
            
    return len(nl)-1 


def makePopulation(num, size):
    population = [range(size) for i in range(num)]
    for t in population:
        random.shuffle(t)
    
    return population


def _scoreOne(one, distances):
    """Score one population member."""
    
    score = 0
    
    for i in range(1, len(one)):
        score += distances[one[i-1]][one[i]]
    return score


def scorePopulation(population, distances):
    """Score an entire population.
    return the scores in a list along with the individual best score and 
    index."""
    scores = [0] * len(population)
    bestScore = -1
    best = -1
    
    for i in range(len(scores)):
        scores[i] = _scoreOne(population[i], distances)
        
        if bestScore == -1 or scores[i] < bestScore:
            bestScore = scores[i]
            best = i
    
    return scores, bestScore, best


def mutate(pop):
    
    v1 = int(random.random() * len(pop))
    v2 = int(random.random() * len(pop))
    
    tmp = pop[v1]
    pop[v1] = pop[v2]
    pop[v2] = tmp
    
    return pop


def mate(pop1, pop2, split):
    """Mate offspring between two parents.
    
    Order does matter as mate will do pop1 before split and pop2 after.
    """
    
    #First determine all repeated elements.
    rIndex = {}
    rValues = {}
    extra = []
    extraIndex = []
    n = [0] * len(pop1)

    #Determine the non included elements and indicies
    for p in range(split):
        rValues[pop2[p]] = 1
        rIndex[pop1[p]] = 1
        
    for p in range(len(pop1) - split):
        if rValues.has_key(pop1[p + split]):
            extra.append(pop1[p + split])
        if rIndex.has_key(pop2[p + split]):
            extraIndex.append(p + split)

    n[0:split] = pop1[0:split]

    #Add in all elements from pop2
    for p in range(len(pop1) - split):
        if len(extraIndex) > 0 and p + split == extraIndex[0]:
            n[p + split] = extra.pop(int(random.random() * len(extra)))
            extraIndex.pop(0)
        else:
            n[p + split] = pop2[p + split]
            
    return n
            

def runGenetic(distances, popSize, \
                mutation = 0.1, \
                iterations = 10000):
    """Perform a basic genetic algorithm.
    
    distances -- n by n matrix of distances
    popSize -- population size
    mutation -- percent of mutation
    """
    
    population = makePopulation(popSize, len(distances))
    bestIndiv = -1
    bestScore = -1

    for i in range(iterations):


        if i % 10 == 0:
            print "Iteration:" + str(i)
        
        scores, bs, b = scorePopulation(population, distances)
        newPop = []

        if bestScore == -1 or bs < bestScore:
            print "New best:" + str(bs)
            bestScore = bs
            bestIndiv = population[b]
        
        #Get a normalized population score to determine who gets
        #to reproduce
        nl = normalizeList(scores)
        
        #Select parents and reproduce with replacement
        for i in range(popSize/2):
            
            #Index of parents
            p1 = population[getParent(nl)]
            p2 = population[getParent(nl)]
            
            split = int(random.random() * len(distances))
            
            #Mate
            off1 = mate(p1, p2, split)
            off2 = mate(p2, p1, split)
            
            #Mutate
            if random.random() < mutate:
                off1 = mutate(off1)

            if random.random() > mutate:
                off2 = mutate(off2)
            
            newPop.append(off1)
            newPop.append(off2)
            
        population = newPop
        population.append(bestIndiv)
        population.append(bestIndiv)
            
    return bestScore, bestIndiv
        

if __name__ == "__main__":
    distances = fileio.readDistances('distances.txt')
    bestScore, bestIndiv = runGenetic(distances, 100)
    
    
    
