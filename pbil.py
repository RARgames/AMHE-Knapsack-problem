import sys
import random
import time
import os
from datetime import datetime
from shutil import copyfile

n = 0
max_weight = 0
items = []
best_knapsack = []


def value(item_set):
    curr_value = 0
    for i in range(0, n):
        if item_set[i] == 1:
            curr_value += items[i][0]
    return curr_value


def weight(item_set):
    curr_weight = 0
    for i in range(0, n):
        if item_set[i] == 1:
            curr_weight += items[i][1]
    return curr_weight


class Pbil:
    def __init__(self, population_size, generations, mutation_probability, mutation_value, learning_rate1, learning_rate2, early_stopping_patience):
        self.population_size = population_size
        self.generations = generations
        self.mutation_probability = mutation_probability
        self.mutation_value = mutation_value
        self.learning_rate1 = learning_rate1
        self.learning_rate2 = learning_rate2
        self.early_stopping_patience = early_stopping_patience

    def run(self, _n, _max_weight, _optimum, _items, _verbose_details):
        start_time = time.time()

        global n, max_weight, items, best_knapsack
        n = _n
        max_weight = _max_weight
        optimum = _optimum
        items = _items
        best_knapsack = [0] * n  # create array filled with zeros of length n, best knapsack so far

        probability_vec = [.5] * n  # initial probability vector
        generation_values = []
        best_values = []
        best_weights = []
        early_stopped = self.generations

        for i in range(0, self.generations):
            if _verbose_details:
                print(f"Processing {i:3} generation:", end=" ")
            else:
                print(".", end="")

            population = self.create_population(probability_vec)
            knapsack, avg_pop_value = self.get_best_knapsack(population)
            alpha = self.evaluate_knapsack(knapsack)
            probability_vec = self.update_prob_vector(alpha, probability_vec)
            probability_vec = self.mutate(probability_vec)

            generation_values.append(avg_pop_value)
            best_values.append(value(knapsack))
            best_weights.append(weight(knapsack))
            if _verbose_details:
                print(f"Current generation avg_value: {avg_pop_value:10.2f}, best knapsack value: {value(knapsack):10}, weight {weight(knapsack):10} for: {knapsack}")
            if self.early_stopping_patience != -1:
                early_stop = 0
                if i > self.early_stopping_patience:
                    first_value = generation_values[-1 - self.early_stopping_patience]
                    # print(f"Checking early stopping: {first_value}", end=" ")
                    j = -1
                    while j > -self.early_stopping_patience - 1:
                        # print(f"{generation_values[j]}", end=" ")
                        # if j == -self.early_stopping_patience:
                        #    print("")
                        if generation_values[j] <= first_value:
                            early_stop += 1
                        j -= 1
                if early_stop >= self.early_stopping_patience:
                    print("Early stopping")
                    early_stopped = i
                    break

        print(f"\nBest knapsack value: {value(best_knapsack)}, weight: {weight(best_knapsack)} for: {best_knapsack}")
        print(f"Problem optimum: {optimum}, max_weight: {max_weight}")
        solving_time = time.time() - start_time
        print(f"The Program took: {solving_time} seconds")
        metrics_path = f"logs/pbil-{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}"
        print(f"Generated files: {metrics_path}.txt, {metrics_path}.csv")
        print(f"Final results added to: logs/final.csv")
        if not os.path.exists("/logs"):
            os.makedirs("/logs")
        copyfile(sys.argv[1], metrics_path + ".txt")
        with open(metrics_path + ".csv", 'a') as file:
            file.write(f"id, avg_value, best_value, best_weight\n")
            for i in range(0, early_stopped):
                file.write(f"{i}, {generation_values[i]}, {best_values[i]}, {best_weights[i]}\n")
        with open("logs/final.csv", 'a') as file:
            if os.stat("logs/final.csv").st_size == 0:
                file.write(f"algorithm_files; n; best_knapsack_value; optimum; best_knapsack_weight; max_weight; solving_time; best_knapsack\n")
            file.write(f"pbil-{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}; {n}; {value(best_knapsack)}; {optimum}; {weight(best_knapsack)}; {max_weight}; {solving_time}; {best_knapsack}\n")

    def create_population(self, probability_vec):
        p = [[0] * n for _ in range(self.population_size)]  # empty 2d array
        for i in range(0, self.population_size):
            for j in range(0, n):
                if random.uniform(0, 1) < probability_vec[j]:
                    p[i][j] = 1
        return p

    def get_best_knapsack(self, population):
        max_value = 0
        max_value_index = -1
        total_value = 0
        for i in range(0, self.population_size):
            if weight(population[i]) <= max_weight:
                curr_value = value(population[i])
                total_value += curr_value
                if curr_value > max_value:
                    max_value = curr_value
                    max_value_index = i
        if max_value_index == -1:  # in case where there is no good candidate
            return [0] * n, total_value / self.population_size
        return population[max_value_index], total_value / self.population_size

    def evaluate_knapsack(self, knapsack):
        global best_knapsack
        if value(best_knapsack) >= value(knapsack):
            alpha = self.learning_rate1
        else:
            alpha = self.learning_rate2
            best_knapsack = knapsack
        return alpha

    def update_prob_vector(self, alpha, probability_vec):
        for i in range(0, n):
            probability_vec[i] = probability_vec[i] * (1 - alpha) + alpha * best_knapsack[i]
        return probability_vec

    def mutate(self, probability_vec):
        for i in range(0, n):
            if random.uniform(0, 1) < self.mutation_probability:
                probability_vec[i] = probability_vec[i] * (1 - self.mutation_value) + random.uniform(0, 1) * self.mutation_value
        return probability_vec
