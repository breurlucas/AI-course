from typing import Coroutine
from genetic_algorithm import GeneticAlgorithm
from city import City
from trip import Trip
import pandas as pd
import random
import math

df_city = pd.read_csv('cities.csv', header=None, index_col=False)
df_travel = pd.read_csv('trips.csv')

# Create blank cities list
cities = []
trips = []

# Genetic parameters
mutationRate = 0.1 # Percentage
crossoverRate = 0.05 # Percentage
mutated = []
crossover = []

indexList = list(range(0,13))

# Populate cities list
for i in range(len(df_city)):
    cities.append(City(df_city.iloc[i, 0],
                       df_city.iloc[i, 1],
                       df_city.iloc[i, 2],
                       df_city.iloc[i, 3],
                       df_city.iloc[i, 4]))

# Populate trips list
for i in range(len(df_travel)):
    trips.append(Trip(df_travel.iloc[i, 0],
                       df_travel.iloc[i, 1],
                       df_travel.iloc[i, 2],
                       df_travel.iloc[i, 3]))


print('Initializing...')
random.seed()

# Initialize population (partial)
genetic = GeneticAlgorithm(indexList, cities, trips)

# Initialize generations count
generations = 0

# Start evolution
while True:

    # Get partial population randomly to mutate
    sample = random.sample(range(0, len(genetic.population)), math.floor(len(genetic.population) * mutationRate))
    mutated = [(genetic.population[i]) for i in sample]

    mutated = [genetic.mutateRemove(individual) for individual in mutated]
    # mutated = [genetic.mutateSwap(individual) for individual in mutated]
    mutated = [genetic.mutateFlip(individual) for individual in mutated]

    # Get partial population randomly to crossover
    sample = random.sample(range(0, len(genetic.population)), math.floor(len(genetic.population) * crossoverRate))
    crossover = [genetic.population[i] for i in sample]

    for i in range(len(crossover) - 1):
        crossover[i] = genetic.crossover(list(crossover[i]), list(crossover[i + 1]))

    generations += 1

    if generations % 1000 == 0:
        genetic.population = genetic.select(genetic.population + mutated + crossover)

    if generations == 8000:
        break

# Check if a solution was found, if so, evaluate
if genetic.fitness(genetic.population[0]) > 0:
    print("\n*** Theft summary ***\n")
    print(genetic.fitness_evaluation(genetic.population[0]))
    print("\nKnapsack items: ")
    mapped = [cities[i] for i in genetic.population[0]]
    for city in mapped:
        text = "{1}, stolen in {0}".format(city.name, city.itemName)
        print(text)

else:
    print("\nFAILED: No valid solution found\n")









# Validation
# for ind in genetic.population:
#     for city in ind:
#         print(city.name)

# print(list(genetic.population[66]))
# flip = genetic.mutateFlip(list(genetic.population[66]), indexList)
# print(flip)

# listPaste = [0,1,2,3,4]
# listCut = [3,4,5]
# mid = 2
# listPaste[:mid] = listCut[:mid]

# print(listPaste)

# print(list(genetic.population[666]))
# value = genetic.fitness(list(genetic.population[1]), cities, trips)
# print(value)
