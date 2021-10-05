# Beatriz Paiva & Lucas Breur
# 10-2021

import itertools
import random
import math

from numpy import empty
from city import City
from trip import Trip

# Travelling Salesman Problem + Knapsack Problem (TSP + KP)
POP_SIZE = 1000

class GeneticAlgorithm():

    # Initialize the population
    def __init__(self, indexList: list[int], cities: list[City], trips: list[Trip]) -> None:
        self.population = []
        self.cities = cities
        self.trips = trips
        self.indexList = indexList
        # Passing through every city, get every possible permutation.
        for i in range(POP_SIZE):
            subset = random.sample(self.indexList, 13)
            self.population.append(subset)

    def fitness(self, individual: list[int]) -> int:
        # Tranform index list in city list (objects)
        mapped = [self.cities[i] for i in individual]

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
            match = False
            for trip in self.trips:
                route = [trip.origin, trip.destination]
                # Checks if there is a connection available, if so, calculates travel cost and time
                if pair == route:
                    time += trip.tripTime # Check total travel time
                    value -= trip.tripCost # Check total travel cost
                    match = True
            if not match: # There is no connection available
                return -100000
        

        # Evaluate time limit, if not exceeded, return value
        if time > 72:
            return -100000

        return value

    # Only to be run on solutions validated with 'fitness'. Returns detailed description
    def fitness_evaluation(self, individual: list[int]) -> int:
        # Tranform index list in city list (objects)
        mapped = [self.cities[i] for i in individual]

        # Initialize variables
        weight = 0
        theftTime = 0
        tripTime = 0
        itemValue = 0
        tripCost = 0

        for city in mapped:
            weight += city.itemWeight # Check total weight
            theftTime += city.theftTime # Check total theft time
            itemValue += city.itemValue # Check total value of all items

        for i in range(len(mapped) - 1):
            pair = [mapped[i].name, mapped[i+1].name]
            for trip in self.trips:
                route = [trip.origin, trip.destination]
                # Checks if there is a connection available, if so, calculates travel cost and time
                if pair == route:
                    tripTime += trip.tripTime # Check total travel time
                    tripCost += trip.tripCost # Check total travel cost

        solution = '''Total value of stolen gooods: {0}$\nTotal weight of stolen goods: {1}kg\nTime spent stealing: {2}h\nTime spent travelling: {3}h\nTravel costs: {4}$\nProfit: {5}$'''.format(itemValue, weight, theftTime, tripTime, tripCost, (itemValue - tripCost))

        return solution

    def select(self, population) -> list:
        # Selection by tragedy. Eliminate 90% of the population
        sortedList = sorted(population, key=self.fitness, reverse=True)
        # Checks if the list is equal or larger than 10 to apply tragedy (For debugging only)
        if len(sortedList) >= 10:
            return sortedList[:math.floor(len(sortedList) * 0.1)]
        
        return sortedList

    def crossover(self, individual1: list[int], individual2: list[int]) -> list:
        # Get shortest individual to cut down
        new1 = list(individual1)
        new2 = list(individual2)
        if len(new1) > len(new2):
            cut = new2
            paste = new1
        else:
            cut = new1
            paste = new2

        # Get rounded down midpoint
        mid = math.floor(len(cut)/2)

        # Copy first halve of one individual to the other
        paste[:mid] = cut[:mid]

        # Replace duplicates in the remaining halve of the new individual (Prevent invalid individuals)
        optionsCutIndexes = [x for x in cut[mid + 1:] if x not in paste[mid + 1:]]
        optionsAllIndexes = [x for x in self.indexList if x not in (cut and paste)]
        for i in range(mid + 1, len(paste)):
            if len(optionsCutIndexes) != 0 and (paste[i] not in optionsCutIndexes):
                paste[i] = optionsCutIndexes[0]
                optionsCutIndexes.pop(0)
            elif len(optionsAllIndexes) != 0 and (paste[i] not in optionsCutIndexes):
                paste[i] = optionsAllIndexes[0]
                optionsAllIndexes.pop(0)
            
        return paste

    def mutateSwap(self, individual: list[int]) -> list:
        new = list(individual)
        if len(individual) > 1:
            positions = sorted(random.sample(range(0, len(new)), 2))
            index_1 = new.pop(positions[0])
            index_2 = new.pop(positions[1] - 1)
            new.insert(positions[0], index_2)
            new.insert(positions[1], index_1)

        return new
    
    def mutateRemove(self, individual: list[int]) -> list:
        new = list(individual)
        for i in range(1, random.randint(1, 13)):
            position = random.randint(0, len(new) - 1)
            # Don't make individuals with less than 3 cities
            if len(new) > 3:
                new.pop(position)
        return new

    def mutateFlip(self, individual: list[int]) -> list:
        new = list(individual)
        # Get options which are not in the individual
        options = [x for x in self.indexList if x not in new]
        # Get random option if available
        if len(options) >= 1:
            newIndex = options[random.randint(0, len(options) - 1)]
            # Remove random index
            position = random.randint(0, len(new) - 1)
            new.pop(position)
            # Insert new index in the same position
            new.insert(position, newIndex)

        return new
