import json
import pbil
import sys


def read_problem_from_file(problem_path):
    items = []
    try:
        with open(problem_path, 'r') as file:
            n, max_weight, optimum = file.readline().split()
            n = int(n)
            max_weight = int(max_weight)
            for i in range(1, n + 1):
                row_items = file.readline().split()
                items.append((int(row_items[1]), int(row_items[2])))
        print(f"Loaded problem from {problem_path}. n={n}, max_weight={max_weight}, items(value, weight)={items}")
        return n, max_weight, optimum, items
    except FileNotFoundError:
        print("Error: Data file not found!")
        exit()


def main(parameters_path):
    try:
        with open(parameters_path, 'r') as file:
            parameters = json.load(file)
    except FileNotFoundError:
        print("Error: Parameters file not found!")
        exit()

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
    repeat_times = parameters.get("repeat_times")

    if algorithm == "p":
        n, max_weight, optimum, items = read_problem_from_file(problem_path)

        solver = pbil.Pbil(population_size, generations, mutation_probability, mutation_value, learning_rate1, learning_rate2, early_stopping_patience)
        for i in range(0, repeat_times):
            solver.run(n, max_weight, optimum, items, verbose_details)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No parameters file specified!')
    else:
        main(sys.argv[1])
