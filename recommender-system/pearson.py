# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

import pandas as pd
import random

# Load data, clear unnecessary columns and set data type
cols1 = ['id', 'title']
cols2 = ['userId', 'movieId', 'rating']
df_movies = pd.read_csv('movies_metadata.csv', dtype={'id': int}, usecols=cols1, encoding='UTF-8')

df_ratings_s = pd.read_csv('ratings_small.csv', dtype={'userId': int, 'movieId': int, 'rating': float}, usecols=cols2, encoding='UTF-8')

# df_ratings = pd.read_csv('ratings.csv', dtype={'userId': int, 'movieId': int, 'rating': float}, usecols=cols2, encoding='UTF-8')

# Rename id to movieId in order to merge
df_movies.rename(columns={"id": "movieId"}, inplace=True)

# Merge both tables by userId
df_merged = df_ratings_s.merge(df_movies, on='movieId')
# print(df_merged)

# Generate pivot table in order to diplay all ratings per movie in columns
df_pivot = df_merged.pivot_table(index='userId', columns='title', values='rating')

# print(list(df_pivot))

# Calculates the Pearson correlation for all movie pairs and saves the values in a new file
# For this we are using the corr function in the pandas library
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html 


corr_matrix = df_pivot.corr(method='pearson', min_periods=1) # Consider only movies with the min amount of ratings

pd.DataFrame(corr_matrix).to_csv('similarities.csv')

# Recommend 10 movies for a new user

# Strategy - Highly rated and diverse
# 1. Pick a selection of users with the hightest amount of ratings given (very active)
# 2. Select highest rated movies by each user
# 3. Pick ten random movies from this selection

most_active_users = df_ratings_s['userId'].value_counts().index.tolist()
most_active_users = most_active_users[:10]
# print(most_active_users)

top_rated = []

for user in most_active_users:
    df = df_ratings_s.loc[df_ratings_s['userId'] == user]
    df = df.sort_values(by = 'rating', ascending=False)
    top_user = df['movieId'].tolist()
    top_rated = top_rated + top_user[:5]

random_top_rated = random.sample(top_rated, 10)

print("Welcome, here are some recommendations for you to get started:\n")
for movie in random_top_rated:
    # print(movie)
    print(df_movies.loc[df_movies['movieId'] == movie, 'title'])

