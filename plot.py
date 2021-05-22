import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("logs/pbil-2021-05-22-21-32-28.csv")
plt.plot(df['id'], df.iloc[:, 1], "r-", label="avg_value")
plt.plot(df['id'], df.iloc[:, 2], "g-", label="best_value")
plt.legend(loc="best")
plt.ylabel('value')
plt.xlabel('generation')
plt.show()
#%%

df1 = pd.read_csv("logs/final.csv", sep=';')
print(df1.iloc[:, 3])
plt.boxplot(df1.iloc[:, 2])
plt.show()
# plt.plot(df1['id'], df1.iloc[:, 3], "r-", label="best_knapsack_value")
# # plt.plot(df['id'], df.iloc[:, 2], "g-", label="best_value")
# plt.legend(loc="best")
# plt.ylabel('value')
# plt.xlabel('generation')

# plt.xlim([1,7])
# plt.ylim([0.3,0.8])