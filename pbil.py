import random

# PBIL parameters
population_size = 20
generations = 100  # total amount of iterations
mutation_probability = 0.2  # from 0 to 1
mutation_value = 0.1  # from 0 to 1
learning_rate1 = 0.1  # from 0 to 1
learning_rate2 = 0.2  # from 0 to 1 and greater than learning_rate1
early_stopping_patience = -1  # int from 1, -1 to skip

items = []
max_weight = 0
n = 0
best_knapsack = []


def read_problem_from_file(path):
    global n, max_weight, best_knapsack
    with open(path) as file:
        n, max_weight = file.readline().split()
        n = int(n)
        max_weight = int(max_weight)
        best_knapsack = [0] * n  # create array filled with zeros of length n, best knapsack so far
        for i in range(1, n + 1):
            row_items = file.readline().split()
            items.append((int(row_items[0]), int(row_items[1])))
    print(f"Loaded problem from {path}. n={n}, max_weight={max_weight}, items(value, weight)={items}")


def value(item_set):
    curr_value = 0
    for i in range(1, n):
        if item_set[i] == 1:
            curr_value += items[i][0]
    return curr_value


def weight(item_set):
    curr_weight = 0
    for i in range(1, n):
        if item_set[i] == 1:
            curr_weight += items[i][1]
    return curr_weight


def create_population(probability_vec):
    # print("create_population", end=" ")
    p = [[0] * n for _ in range(population_size)]  # empty 2d array
    for i in range(1, population_size):
        for j in range(0, n):
            if random.uniform(0, 1) < probability_vec[j]:
                p[i][j] = 1
    return p


def get_best_knapsack(population):
    # print("get_best_knapsack", end=" ")
    max_value = 0
    max_value_index = -1
    for i in range(1, population_size):
        if weight(population[i]) <= max_weight:
            curr_value = value(population[i])
            if curr_value > max_value:
                max_value = curr_value
                max_value_index = i
    if max_value_index == -1:  # in case where there is no good candidate
        return [0] * n
    return population[max_value_index]


def evaluate_knapsack(knapsack):
    global best_knapsack
    if value(best_knapsack) >= value(knapsack):
        alpha = learning_rate1
    else:
        alpha = learning_rate2
        best_knapsack = knapsack
    return alpha


def update_prob_vector(alpha, probability_vec):
    # print("update_prob_vector", end=" ")
    for i in range(1, n):
        probability_vec[i] = probability_vec[i] * (1 - alpha) + alpha * best_knapsack[i]
    return probability_vec


def mutate(probability_vec):
    # print("mutate")
    for i in range(1, n):
        if random.uniform(0, 1) < mutation_probability:
            probability_vec[i] = probability_vec[i] * (1 - mutation_value) + random.uniform(0, 1) * mutation_value
    return probability_vec


def pbil():
    read_problem_from_file("problems/f1_l-d_kp_10_269")
    probability_vec = [.5] * n  # initial probability vector
    curr_generation = 1
    generation_value = []
    for i in range(1, generations):
        print(f"Processing {curr_generation:2} generation:", end=" ")
        population = create_population(probability_vec)
        knapsack = get_best_knapsack(population)
        alpha = evaluate_knapsack(knapsack)
        probability_vec = update_prob_vector(alpha, probability_vec)
        probability_vec = mutate(probability_vec)

        generation_value.append(value(knapsack))
        print(f"Current generation best knapsack: {knapsack}, Value: {value(knapsack)}, Weight {weight(knapsack)}")
        if early_stopping_patience != -1:
            early_stop = 0
            if curr_generation > early_stopping_patience:
                first_value = generation_value[-1 - early_stopping_patience]
                print(f"Checking early stopping: {first_value}", end=" ")
                j = -1
                while j > -early_stopping_patience - 1:
                    print(f"{generation_value[j]}", end=" ")
                    if j == -early_stopping_patience:
                        print("")
                    if generation_value[j] <= first_value:
                        early_stop += 1
                    j -= 1
            if early_stop >= early_stopping_patience:
                print("Early stopping")
                break
        curr_generation += 1
    print(f"\nBest knapsack: {best_knapsack}, Value: {value(best_knapsack)}, Weight: {weight(best_knapsack)}")


if __name__ == '__main__':
    pbil()

# TODO parametry do pliku
# TODO wykresy ----- jak zbierac dane
# TODO sprawdzanie czasu wykonywania algorytmu
# TODO przeniesienie do osobnego pliku
