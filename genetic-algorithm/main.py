from genetic_algorithm import GeneticAlgorithm
from city import City
import pandas as pd
import random

df_city = pd.read_csv('cities.csv', header=None, index_col=False)
df_travel = pd.read_csv('travel.csv')

# Create blank cities list
cities = []
indexList = list(range(0,13))

# Populate cities list
for i in range(len(df_city)):
    cities.append(City(df_city.iloc[i, 0],
                       df_city.iloc[i, 1],
                       df_city.iloc[i, 2],
                       df_city.iloc[i, 3],
                       df_city.iloc[i, 4]))

print('Initializing...')
random.seed()

genetic = GeneticAlgorithm(indexList)

print(len(genetic.population))

# for ind in genetic.population:
#     for city in ind:
#         print(city.name)

# Validation
# print(list(genetic.population[66]))
# flip = genetic.mutateFlip(list(genetic.population[66]), indexList)
# print(flip)

listPaste = [0,1,2,3,4]
listCut = [3,4,5]
mid = 2
listPaste[:mid] = listCut[:mid]

print(listPaste)
