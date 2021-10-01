# Beatriz Paiva & Lucas Breur
# 10-2021


import itertools
import random
import math

# Travelling Salesman Problem + Knapsack Problem (TSP + KP)

MAX_SEQ_SIZE = 5

class GeneticAlgorithm():

    # Initialize the population
    def __init__(self, indexList) -> None:
        self.population = []
        # Passing through every city, get every possible permutation.
        for subset in itertools.permutations(indexList, MAX_SEQ_SIZE):
            self.population.append(subset)

    def fitness(self) -> int:
        return 1

    def select(cls) -> int:
        return 1

    def crossover(self, list1, list2) -> list:
        # Get shortest list to cut down
        if len(list1) > len(list2):
            listCut = list2
            listPaste = list1
        else:
            listCut = list1
            listPaste = list2

        # Get rounded down midpoint
        mid = math.floor(len(listCut)/2)

        # Copy first halve of one list to the other
        listPaste[:mid] = listCut[:mid]

        # Replace duplicates in the remaining halve of the new list (Prevent invalid individuals)
        # options = [x for x in indexList if x not in list]
        # listPaste[mid + 1:]
            
        return listPaste

    def mutateSwap(self, list) -> list:
        positions = sorted(random.sample(range(0, len(list)), 2))
        print(positions)
        index_1 = list.pop(positions[0])
        print(index_1)
        index_2 = list.pop(positions[1] - 1)
        print(index_2)

        list.insert(positions[0], index_2)
        list.insert(positions[1], index_1)

        return list
    
    def mutateRemove(self, list) -> list:
        if len(list) > 1:
            position = random.randint(0, len(list) - 1)
            list.pop(position)
        return list

    def mutateFlip(self, list, indexList) -> list:
        # Get options which are not in list
        options = [x for x in indexList if x not in list]
        print(options)
        # Get random option
        newIndex = options[random.randint(0, len(options) - 1)]
        print(newIndex)
        # Remove random index
        position = random.randint(0, len(list) - 1)
        list.pop(position)
        # Insert new index in the same position
        list.insert(position, newIndex)

        return list
