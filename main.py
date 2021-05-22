import json
import pbil


def read_problem_from_file(problem_path):
    items = []
    with open(problem_path, 'r') as file:
        n, max_weight = file.readline().split()
        n = int(n)
        max_weight = int(max_weight)
        for i in range(1, n + 1):
            row_items = file.readline().split()
            items.append((int(row_items[0]), int(row_items[1])))
    print(f"Loaded problem from {problem_path}. n={n}, max_weight={max_weight}, items(value, weight)={items}")
    return n, max_weight, items


def main():
    with open("parameters.json", 'r') as file:
        parameters = json.load(file)
    problem_path = parameters.get("problem_path")
    population_size = parameters.get("population_size")
    generations = parameters.get("generations")
    mutation_probability = parameters.get("mutation_probability")
    mutation_value = parameters.get("mutation_value")
    learning_rate1 = parameters.get("learning_rate1")
    learning_rate2 = parameters.get("learning_rate2")
    early_stopping_patience = parameters.get("early_stopping_patience")

    solver = pbil.Pbil(population_size, generations, mutation_probability, mutation_value, learning_rate1, learning_rate2, early_stopping_patience)
    n, max_weight, items = read_problem_from_file(problem_path)
    solver.run(n, max_weight, items)


if __name__ == '__main__':
    main()

# TODO wykresy ----- jak zbierac dane
# TODO sprawdzanie czasu wykonywania algorytmu
