import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numpy as np


df = pd.read_csv("log_avgFit07_06_2021_12_37_05.csv")
plt.plot(df['generation_counter'], df.iloc[:, 1], "r-", label="fitness")
plt.plot(df['generation_counter'], df.iloc[:, 2], "g-", label="best_fitness")
plt.legend(loc="best")
plt.ylabel('value')
plt.xlabel('generation')
plt.show()

