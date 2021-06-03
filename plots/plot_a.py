#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import pandas as pd



FILENAME = sys.argv[1]

#%matplotlib inline  # jupyter notebook


# Load data
data = pd.read_csv(f'{FILENAME}.csv')

# Plot fitness
#plt.figure(figsize=(10, 5))
x = range(len(data['fitness']))
y = range(len(data['fitness']))
plt.plot(x, data['fitness'])
#plt.xticks(x, data['generation_counter'])
plt.xlabel('generation_counter')
plt.ylabel('fitness')
#plot
plt.show()


