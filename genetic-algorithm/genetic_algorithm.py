# Beatriz Paiva & Lucas Breur
# 10-2021

import itertools
import random
import math
from city import City
from trip import Trip

# Travelling Salesman Problem + Knapsack Problem (TSP + KP)

MAX_SEQ_SIZE = 5

class GeneticAlgorithm():

    # Initialize the population
    def __init__(self, indexList: list[int]) -> None:
        self.population = []
        # Passing through every city, get every possible permutation.
        for subset in itertools.permutations(indexList, MAX_SEQ_SIZE):
            self.population.append(subset)

    def fitness(self, individual: list[int], cities: list[City], trips: list[Trip]) -> int:
        # Tranform index list in city list (objects)
        mapped = [cities[i] for i in individual]

        # Initialize variables
        weight = 0
        time = 0
        value = 0

        for city in mapped:
            weight += city.itemWeight # Check total weight
            time += city.theftTime # Check total theft time
            value += city.itemValue # Check total value of all items
        
        # Evaluate weight limit, if not exceeded, proceed to calculate travel time and cost
        if weight > 20:
            return -100000

        for i in range(len(mapped) - 1):
            pair = [mapped[i].name, mapped[i+1].name]
            print(pair)
            match = False
            for trip in trips:
                route = [trip.origin, trip.destination]
                # Checks if there is a connection available, if so, calculates travel cost and time
                if pair == route:
                    time += trip.tripTime # Check total travel time
                    value -= trip.tripCost # Check total travel cost
                    match = True
                    print(route)
            if not match: # There is no connection available
                return - 100000
        

        # Evaluate time limit, if not exceeded, return value
        if time > 72:
            return -100000

        return value

    def select(cls) -> int:
        return 1

    def crossover(self, individual1: list[int], individual2: list[int]) -> list:
        # Get shortest individual to cut down
        if len(individual1) > len(individual2):
            cut = individual2
            paste = individual1
        else:
            cut = individual1
            paste = individual2

        # Get rounded down midpoint
        mid = math.floor(len(cut)/2)

        # Copy first halve of one individual to the other
        paste[:mid] = cut[:mid]

        # Replace duplicates in the remaining halve of the new individual (Prevent invalid individuals)
        # options = [x for x in indexList if x not in list]
        # paste[mid + 1:]
            
        return paste

    def mutateSwap(self, individual: list[int]) -> list:
        positions = sorted(random.sample(range(0, len(individual)), 2))
        print(positions)
        index_1 = individual.pop(positions[0])
        print(index_1)
        index_2 = individual.pop(positions[1] - 1)
        print(index_2)

        individual.insert(positions[0], index_2)
        individual.insert(positions[1], index_1)

        return individual
    
    def mutateRemove(self, individual: list[int]) -> list:
        if len(individual) > 1:
            position = random.randint(0, len(individual) - 1)
            individual.pop(position)
        return individual

    def mutateFlip(self, individual: list[int], indexList: list[int]) -> list:
        # Get options which are not in the individual
        options = [x for x in indexList if x not in individual]
        # Get random option
        newIndex = options[random.randint(0, len(options) - 1)]
        # Remove random index
        position = random.randint(0, len(individual) - 1)
        individual.pop(position)
        # Insert new index in the same position
        individual.insert(position, newIndex)

        return individual
