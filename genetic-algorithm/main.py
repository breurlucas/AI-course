from genetic_algorithm import GeneticAlgorithm
from city import City
from trip import Trip
import pandas as pd
import random

df_city = pd.read_csv('cities.csv', header=None, index_col=False)
df_travel = pd.read_csv('trips.csv')

# Create blank cities list
cities = []
trips = []

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
genetic = GeneticAlgorithm(indexList)

# Initialize generations count
generations = 0

# Start evolution
while generations <= 1000:
    
    mutated = [mutar(individuo) for individuo in populacao]
    crossover = crossover(populacao, pop_mutada)
    selection = genetic.select(population + mutated + crossover)
    
    generations += 1



print('Done!')


# for ind in genetic.population:
#     for city in ind:
#         print(city.name)

# Validation
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
