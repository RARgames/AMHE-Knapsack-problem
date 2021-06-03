import os
import pandas

for filename in os.listdir("logs"):
    df = pandas.read_csv(f"logs/{filename}/final.csv", sep=";")
    print(f"{filename}")
    print(df.describe())