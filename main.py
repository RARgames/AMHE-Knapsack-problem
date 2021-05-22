import json
import pbil
import sys


def read_problem_from_file(problem_path):
    items = []
    with open(problem_path, 'r') as file:
        n, max_weight, optimum = file.readline().split()
        n = int(n)
        max_weight = int(max_weight)
        for i in range(1, n + 1):
            row_items = file.readline().split()
            items.append((int(row_items[0]), int(row_items[1])))
    print(f"Loaded problem from {problem_path}. n={n}, max_weight={max_weight}, items(value, weight)={items}")
    return n, max_weight, optimum, items


def main(parameters_path):
    with open(parameters_path, 'r') as file:
        parameters = json.load(file)
    algorithm = parameters.get("algorithm")
    verbose_details = parameters.get("verbose_details")
    problem_path = parameters.get("problem_path")
    population_size = parameters.get("population_size")
    generations = parameters.get("generations")
    mutation_probability = parameters.get("mutation_probability")
    mutation_value = parameters.get("mutation_value")
    learning_rate1 = parameters.get("learning_rate1")
    learning_rate2 = parameters.get("learning_rate2")
    early_stopping_patience = parameters.get("early_stopping_patience")

    n, max_weight, optimum, items = read_problem_from_file(problem_path)

    if algorithm == "p":
        solver = pbil.Pbil(population_size, generations, mutation_probability, mutation_value, learning_rate1, learning_rate2, early_stopping_patience)
        solver.run(n, max_weight, optimum, items, verbose_details)
    # else:
    #     solver = ga.Genetic()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No parameters file specified!')
    else:
        main(sys.argv[1])

# TODO plots + sufficient data?
# http://www.dcs.gla.ac.uk/~pat/cpM/jchoco/knapsack/papers/hardInstances.pdf
# http://hjemmesider.diku.dk/~pisinger/codes.html
# http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/
# http://galera.ii.pw.edu.pl/~skozdrow/AMHE/amhe_SK_lato_2021.pdf
# https://www.researchgate.net/publication/343738629_Adaptive_Algorithms_for_solving_the_Knapsack_Problem#pfb
# https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
