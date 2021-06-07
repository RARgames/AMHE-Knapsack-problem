import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("logs/p_knapPI_3_100_1000/pbil-2021-06-03-23-00-19.csv")
plt.plot(df['id'], df.iloc[:, 1], "r-", label="avg_value")
plt.plot(df['id'], df.iloc[:, 2], "g-", label="best_value")
plt.legend(loc="best")
plt.ylabel('value')
plt.xlabel('generation')
plt.show()

#%%
df1 = pd.read_csv("logs/p_knapPI_3_100_1000/final.csv", sep=';')
plt.boxplot(df1.iloc[:, 2])
plt.ylabel('best_knapsack_value')
plt.show()

#%%
for filename in os.listdir("logs"):
    df = pd.read_csv(f"logs/{filename}/final.csv", sep=";")
    print(f"{filename}")
    print(df.describe())