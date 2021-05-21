import random

population_size = 5
max_weight = 25
# weights = [12, 7, 11, 8, 9]
# prices = [24, 13, 23, 15, 16]
items = [(12, 24), (7, 13), (11, 23), (8, 15), (9, 16)]
# TODO get from the file
n = len(items)  # number of all items
best_knapsack = [0] * n  # create array filled with zeros of length n, best knapsack so far


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


def create_population(v):
    print("create")
    p = [[0]*n for i in range(population_size)]  # empty 2d array
    j = random.randint(0, n)
    j += 1
    for i in range(1, population_size):
        for j in range(1, n):
            r = random.uniform(0, 1)
            if v[j] > r:
                p[i][j] = 1
            if weight(p[i]) > max_weight:
                j = 0
    # print("population {}", p)
    return p


def get_best_knapsack(p):
    print("get")
    max_value = 0
    max_value_index = 0
    for i in range(1, population_size):
        curr_value = value(p[i])
        if curr_value > max_value:
            max_value = curr_value
            max_value_index = i
    return p[max_value_index]


def update_prob_vector(knapsack, v):
    print("update")
    alpha1 = 0.1  # learning rate 1
    alpha2 = 0.2  # learning rate 2 - greater than alpha1
    global best_knapsack
    if value(best_knapsack) >= value(knapsack):
        alpha = alpha1
    else:
        alpha = alpha2
        best_knapsack = knapsack
    for i in range(1, n):
        v[i] = v[i] * (1 - alpha) + alpha * best_knapsack[i]
    return v


def mutate(v):
    print("v")
    m_v = 0.1  # mutation value #TODO to properties
    m_p = 0.2  # mutation probability #TODO to properties
    for i in range(1, n):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        if m_p > r1:
            v[i] = v[i] * (1 - m_v)
            if r2 > 0.5 and v[i] + m_v <= 1:
                v[i] = v[i] + m_v
    return v


def main():
    knapsack = best_knapsack
    # p = # create empty 2d array
    v = [.5] * n  # probability vector
    max_iter = 20  # total amount of iterations # TODO increase to 100

    for i in range(1, max_iter):
        p = create_population(v)
        knapsack = get_best_knapsack(p)
        v = update_prob_vector(knapsack, v)
        v = mutate(v)
    print("Best knapsack: {}, Value: {}, Weight: {}".format(knapsack, value(knapsack), weight(knapsack)))
    #return knapsack


if __name__ == '__main__':
    main()
