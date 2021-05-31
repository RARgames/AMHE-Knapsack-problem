import random
import sys
import operator
import math
import time
import csv
from datetime import datetime

UL_ALGORITHM_TYPE = sys.argv[8]

UL_FILENAME = sys.argv[1]
N = int(sys.argv[2])
THREE = sys.argv[3]
UL_FOUR = sys.argv[4]
UL_FIVE = float(sys.argv[5])
UL_SIX = float(sys.argv[6])
UL_GENERATIONS = int(sys.argv[7])

M = 2
k = 1

header = ['generation_counter', 'fitness', 'best_fitness']
w, h = 3, UL_GENERATIONS;
data = [[0 for x in range(w)] for y in range(h)]

UL_header_knap_val = ['generation_counter', 'sum(fitness)']
data_knap_val = [[0 for x in range(2)] for y in range(UL_GENERATIONS)]


def UL_read_in_file_GA(file_name):
    UL_test_object = open(file_name, 'r')
    data = UL_test_object.readlines()
    UL_out = []
    UL_firstline = data[0].split(' ')
    num_var = UL_firstline[2]
    num_clauses = UL_firstline[3]
    for line in range(1, len(data)):
        UL_out.append(data[line].split(' ')[:-1])
    UL_test_object.close()
    return (UL_out, int(num_var), int(num_clauses))

PROBLEM, NUM_VAR, NUM_CLAUSES = UL_read_in_file_GA(UL_FILENAME)


def UL_generate_individual():
    individual = []

    for num in range(int(NUM_VAR)):
        individual.append(random.choice([True, False]))
    return individual


def UL_generate_population():
    population = []

    for num in range(N):
        population.append(UL_generate_individual())
    return population


def UL_evaluate_fitness(population):
    population_clauses = []

    for i in range(N):
        clause_count = 0
        for clause in PROBLEM:
            for var in clause:
                if int(var) < 0:
                    if population[i][abs(int(var)) - 1] == False:
                        clause_count += 1
                        break
                    else:
                        continue
                else:
                    if population[i][int(var) - 1] == True:
                        clause_count += 1
                        break
                    else:
                        continue
        population_clauses.append(clause_count)
    return population_clauses


def UL_select_individual_rank(ranks, sum_ranks):
    rand_num = random.randint(1, sum_ranks)
    running_total = 0

    for rank in ranks:
        running_total += int(rank)
        if running_total >= rand_num:
            return rank
        else:
            continue
    return -1


def UL_ranked_selection(population, fitness):
    new_list = zip(population, fitness)
    sorted_by_second = sorted(list(new_list), key=lambda tup: tup[1])
    pop, fit = zip(*sorted_by_second)
    good_list = zip(pop, fit, list(range(1, N + 1)))
    pop, fit, ranks = zip(*good_list)
    pop_list = list(pop)
    fit_list = list(fit)
    ranks_list = list(ranks)
    rank_sum = sum(ranks_list)
    breeding_pool_ranks = []

    for num in range(N):
        breeding_pool_ranks.append(UL_select_individual_rank(ranks_list, rank_sum))
    breeding_pool = []
    for rank in breeding_pool_ranks:
        breeding_pool.append(pop_list[rank - 1])
    return breeding_pool


def UL_tournament_selection(population, fitness):
    breeding_pool = []

    for i in range(int((N / k))):
        tournament_pool = []
        for j in range(M):
            rand_num = random.randint(0, N - 1)
            tournament_pool.append((population[rand_num], fitness[rand_num]))
        winner = max(tournament_pool, key=operator.itemgetter(1))[0]
        breeding_pool.append(winner)
    return breeding_pool


def UL_Boltzmann_select_one(b_fitnesses, b_sum):
    rand_num = random.uniform(0, b_sum)
    running_total = 0
    index_counter = 0

    for fit in b_fitnesses:
        running_total += fit
        if running_total >= rand_num:
            return index_counter
        else:
            index_counter += 1
            continue
    return 100


def UL_Boltzmann_selection(population, fitness):
    boltzmann_fitnesses = []

    for fit in fitness:
        b_fitness = math.exp(fit)
        boltzmann_fitnesses.append(b_fitness)
    boltzmann_sum = sum(boltzmann_fitnesses)
    breeding_pool_indices = []
    for num in range(N):
        breeding_pool_indices.append(UL_Boltzmann_select_one(boltzmann_fitnesses, boltzmann_sum))
    breeding_pool = []
    for ind in breeding_pool_indices:
        breeding_pool.append(population[ind])
    return breeding_pool


def UL_one_point_crossover(breeding_pool):
    count = 0
    new_pop = []

    while count < N:
        parent1_rand = random.randint(0, N - 1)
        parent2_rand = random.randint(0, N - 1)
        parent1 = breeding_pool[parent1_rand]
        parent2 = breeding_pool[parent2_rand]
        rand_num = random.uniform(0.0, 1.0)
        if rand_num <= UL_FIVE:
            rand_point = random.randint(1, NUM_VAR - 1)
            parent1_end = parent1[rand_point:]
            parent2_end = parent2[rand_point:]
            child1 = parent1[:rand_point] + parent2_end
            child2 = parent2[:rand_point] + parent1_end
            new_pop.append(child1)
            new_pop.append(child2)
            count += 2
        else:
            new_pop.append(parent1)
            new_pop.append(parent2)
            count += 2
    if len(new_pop) > N:
        new_pop.pop()
    return new_pop


def UL_uniform_crossover(breeding_pool):
    count = 0
    new_pop = []

    while count < N:
        parent1_rand = random.randint(0, N - 1)
        parent2_rand = random.randint(0, N - 1)
        parent1 = breeding_pool[parent1_rand]
        parent2 = breeding_pool[parent2_rand]
        rand_num = random.uniform(0.0, 1.0)

        if rand_num <= UL_FIVE:
            child = []
            for i in range(NUM_VAR):
                parent_decision = random.uniform(0.0, 1.0)
                if parent_decision <= 0.5:
                    child.append(parent1[i])
                else:
                    child.append(parent2[i])
            new_pop.append(child)
            count += 1
        else:
            new_pop.append(parent1)
            new_pop.append(parent2)
            count += 2
    if len(new_pop) > N:
        new_pop.pop()
    return new_pop


def UL_mutation(current_pop):
    final_pop = current_pop

    for i in range(N):
        for j in range(NUM_VAR):
            rand_num = random.uniform(0.0, 1.0)
            if rand_num <= UL_SIX:
                final_pop[i][j] = not final_pop[i][j]
            else:
                continue
    return final_pop


def UL_genetic_algorithm():
    generation_counter = 0
    best_fitness = 0
    population = UL_generate_population()

    while generation_counter < UL_GENERATIONS:
        generation_counter += 1
        fitness = UL_evaluate_fitness(population)
        best_index, best_value = max(enumerate(fitness), key=operator.itemgetter(1))
        if best_value > best_fitness:
            best_fitness = best_value
            best_solution = population[best_index]
            best_solution_print = str(best_solution)
            best_solution_print = best_solution_print.replace("True", "1")
            best_solution_print = best_solution_print.replace("False", "0")
            print(
                f"Current generation {generation_counter}, avarage fitness : {sum(fitness) / len(fitness)}, best fitness value: {best_fitness}"
                f",value of knapsack: {sum(fitness)}, best value find in this generation:{best_solution_print}\n")
        else:
            print(f"Current generation {generation_counter}, avarage fitness: {sum(fitness) / len(fitness)},"
                  f"best fitness value: {best_fitness}, value of knapsack: {sum(fitness)}")
        data[generation_counter - 1][0] = generation_counter
        data[generation_counter - 1][1] = sum(fitness) / len(fitness)
        data[generation_counter - 1][2] = best_fitness
        data_knap_val[generation_counter - 1][0] = generation_counter
        data_knap_val[generation_counter - 1][1] = sum(fitness)
        if best_fitness == NUM_CLAUSES:
            print("================Global best opimal found")
            break
        if THREE == "rs":
            breeding_pool = UL_ranked_selection(population, fitness)
        elif THREE == "ts":
            breeding_pool = UL_tournament_selection(population, fitness)
        elif THREE == "bs":
            breeding_pool = UL_Boltzmann_selection(population, fitness)
        if UL_FOUR == "1c":
            current_pop = UL_one_point_crossover(breeding_pool)
        elif UL_FOUR == "uc":
            current_pop = UL_uniform_crossover(breeding_pool)
        population = UL_mutation(current_pop)

    print("The UL_FILENAME for this problem is: " + UL_FILENAME)
    print("Number of variables: " + str(NUM_VAR))
    print("Number of clauses: " + str(NUM_CLAUSES))
    print("Number of clauses satisfied: " + str(best_fitness))
    print("Percentage of clauses satisfied: " + "{}%".format((best_fitness / float(NUM_CLAUSES)) * 100))
    best_solution = str(best_solution)
    best_solution = best_solution.replace("True", "1")
    best_solution = best_solution.replace("False", "0")
    print("Solution: " + str(best_solution))
    print("This solution was found during iteration: " + str(generation_counter))
    print()

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    with open(f'log_avgFit{dt_string}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    with open(f'log_knapVal{dt_string}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(UL_header_knap_val)
        writer.writerows(data_knap_val)


def main():
    input_list = sys.argv[1:]
    if len(input_list) != 8:
        print("Error... must accept 8 command line arguments")
        return
    start_time = time.time()

    if UL_ALGORITHM_TYPE == 'g':
        UL_genetic_algorithm()
    print("The Program took: " + str(time.time() - start_time) + " seconds")

if __name__ == '__main__':
    main()

