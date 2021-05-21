import random

population_size = 20
max_weight = 26
items = [(12, 24), (7, 13), (11, 23), (8, 15), (9, 16)]
n = len(items)  # number of all items
best_knapsack = [0] * n  # create array filled with zeros of length n, best knapsack so far
generations = 20  # total amount of iterations
mutation_probability = 0.2  # from 0 to 1
mutation_value = 0.1  # from 0 to 1


def value(item_set):
    curr_value = 0
    for i in range(1, n):
        if item_set[i] == 1:
            curr_value += items[i][1]
    return curr_value


def weight(item_set):
    curr_weight = 0
    for i in range(1, n):
        if item_set[i] == 1:
            curr_weight += items[i][0]
    return curr_weight


def create_population(probability_vec):
    print("create_population")
    p = [[0] * n for _ in range(population_size)]  # empty 2d array
    for i in range(1, population_size):
        for j in range(0, n):
            r = random.uniform(0, 1)
            if probability_vec[j] > r:
                p[i][j] = 1
    return p


def get_best_knapsack(population):
    print("get_best_knapsack")
    max_value = 0
    max_value_index = -1
    for i in range(1, population_size):
        if weight(population[i]) <= max_weight:
            curr_value = value(population[i])
            if curr_value > max_value:
                max_value = curr_value
                max_value_index = i
    if max_value_index == -1:  # in case where there is no good candidate - try to fix it
        return [0] * n  # empty array of length n
    return population[max_value_index]


def update_prob_vector(knapsack, probability_vec):
    print("update_prob_vector")
    learning_rate1 = 0.1
    learning_rate2 = 0.2  # greater than learning_rate1
    global best_knapsack
    # print("x ", best_knapsack)
    # print("xd ", knapsack)
    if value(best_knapsack) >= value(knapsack):
        alpha = learning_rate1
    else:
        alpha = learning_rate2
        best_knapsack = knapsack
    for i in range(1, n):
        probability_vec[i] = probability_vec[i] * (1 - alpha) + alpha * best_knapsack[i]
    return probability_vec


def mutate(probability_vec):
    print("mutate")
    for i in range(1, n):
        r2 = random.uniform(0, 1)
        if mutation_probability > random.uniform(0, 1):
            probability_vec[i] = probability_vec[i] * (1 - mutation_value)
            if r2 > 0.5 and probability_vec[i] + mutation_value <= 1:
                probability_vec[i] = probability_vec[i] + mutation_value
    return probability_vec


def pbil():
    knapsack = best_knapsack
    probability_vec = [.5] * n  # initial probability vector
    for i in range(1, generations):
        population = create_population(probability_vec)
        knapsack = get_best_knapsack(population)
        probability_vec = update_prob_vector(knapsack, probability_vec)
        probability_vec = mutate(probability_vec)
    print("Best knapsack: {}, Value: {}, Weight: {}".format(knapsack, value(knapsack), weight(knapsack)))


if __name__ == '__main__':
    pbil()
