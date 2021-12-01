# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

# Uses the custom pip package gym-parking_lot at: https://github.com/breurlucas/gym-parking_lot

# Resources for the Q-learning section: https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/

import gym
import sys, os, time
import numpy as np
import random

# Animate solution
def animate(frames):
    clear_console = 'clear' if os.name == 'posix' else 'CLS'

    while True:
        for frame in frames:

            # Clear the console
            os.system(clear_console)

            # Write the current frame on stdout and sleep
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(0.1)

env = gym.make("gym_parking_lot:parking_lot-v0").env

# Initialize Q-table
q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Set Q-learning parameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

frames = []
itr = 100000

# Train AI
for i in range(1, itr + 1):

    # Reset for new run
    state = env.reset()
    reward = 0
    done = False
    
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, info = env.step(action) 
        
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        state = next_state

        if i == itr:
            frames.append(env.render(mode='ansi'))

print("Training finished.\n")
# print(q_table)
animate(frames)
