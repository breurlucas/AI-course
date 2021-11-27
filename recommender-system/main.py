# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

import pandas as pd

# Load similarities file
df_similarities = pd.read_csv('similarities.csv')

# Recommend 10 movies based on previously liked title

liked = ['20,000 Leagues Under the Sea', 'Rocky IV', '2001: A Space Odyssey', '48 Hrs.', 'A Nightmare on Elm Street']

i = 0
for movie in liked:
    print(f'\nUser {i+1}, we see you liked {liked[i]}, here are some recommendations: \n')
    print(df_similarities.corr()[liked[i]].sort_values(ascending=False).iloc[:10])
    i+=1


