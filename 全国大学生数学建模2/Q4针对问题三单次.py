import numpy as np
import scipy.stats as stats



def normal_sampling(mean, std_dev, size=1):
    return np.random.normal(loc=mean, scale=std_dev, size=size)

def fitness_function(decision, components, subassemblies, product):
    total_s = 0
    total_c = 0
    total_i = 0
    total_d = 0

    for i, comp in enumerate(components):
        sampled_d_r = max(0, normal_sampling(comp['defect_rate'], comp['defect_rate'] * 0.1))
        print(sampled_d_r)
        if decision[i]:
            total_s += comp['cost'] * sampled_d_r
            total_c += comp['inspect_cost']
            total_i += 1
        else:
            total_c += comp['cost'] * sampled_d_r
            total_d += 1

    subassembly_s = len(components)
    for j, subass in enumerate(subassemblies):
        sampled_d_r = max(0, normal_sampling(subass['defect_rate'], subass['defect_rate'] * 0.1))
        print(sampled_d_r)
        inspect_c = subass['inspect_cost']
        defect_c = subass['assembly_cost'] * sampled_d_r
        disassemble_cost = subass['disassemble_cost']

        if decision[subassembly_s + j]:
            total_s += defect_c
            total_c += inspect_c
            total_i += 1
        else:
            total_c += defect_c
            total_d += 1

    product_s = subassembly_s + len(subassemblies)
    sampled_d_r = max(0, normal_sampling(product['defect_rate'], product['defect_rate'] * 0.1))
    print(sampled_d_r)
    inspect_c = product['inspect_cost']
    defect_c = product['assembly_cost'] * sampled_d_r
    disassemble_cost = product['disassemble_cost']

    if decision[product_s]:
        total_s += defect_c
        total_c += inspect_c
        total_i += 1
    else:
        total_c += defect_c
        total_d += 1

    profit = product['sale_price'] - total_c - product['replacement_loss'] + total_s

    fitness = total_s - total_c + abs(total_c)
    return fitness, profit, total_i, total_d


def genetic_algorithm(components, subassemblies, product, population_size=50, generations=100, mutation_rate=0.01):
    decision_length = len(components) + len(subassemblies) + 1
    population = [np.random.choice([0, 1], decision_length) for _ in range(population_size)]

    b_decisions = []
    b_fitnesses = []
    b_profits = []

    for generation in range(generations):
        fit_p = [fitness_function(individual, components, subassemblies, product) for individual in
                                 population]
        fitnesses = [fit[0] for fit in fit_p]
        profits = [profit for _, profit, _, _ in fit_p]

        parents = selection(population, fitnesses)

        offspring = crossover(parents)

        mutated_o = mutate(offspring, mutation_rate)

        population = replace(population, mutated_o, fitnesses)

        best_individual = max(population, key=lambda ind: fitness_function(ind, components, subassemblies, product)[0])
        best_fitness, best_profit, best_inspection, best_defect = fitness_function(best_individual, components,
                                                                                   subassemblies, product)
        b_decisions.append(best_individual)
        b_fitnesses.append(best_fitness)
        b_profits.append(best_profit)

    final_best_i = max(b_decisions,
                                key=lambda ind: fitness_function(ind, components, subassemblies, product)[0])
    final_best_f, final_best_p, final_best_i, final_best_d = fitness_function(
        final_best_i, components, subassemblies, product)

    print(f"Final Best decision: {final_best_i}")
    print(f"Final Best fitness: {final_best_f}")
    print(f"Final Best profit: {final_best_p}")
    print(f"Total inspection decisions: {final_best_i}")
    print(f"Total defect decisions: {final_best_d}")

    for gen, (decision, fitness, profit) in enumerate(zip(b_decisions, b_fitnesses, b_profits)):
        fitness, profit, inspection, defect = fitness_function(decision, components, subassemblies, product)
        print(
            f"Generation {gen + 1}: Best decision: {decision}, Best fitness: {fitness}, Best profit: {profit}, Inspection: {inspection}, Defect: {defect}")

    return final_best_i, final_best_f, final_best_p

def selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    probabilities = [f / total_fitness for f in fitnesses]

    probabilities = np.array(probabilities)

    probabilities /= probabilities.sum()

    num_parents = min(2, len(population))

    indices = np.arange(len(population))

    probabilities_1d = probabilities.ravel()

    selected_indices = np.random.choice(indices, size=num_parents, replace=False, p=probabilities_1d)

    parents = [population[i] for i in selected_indices]
    return parents


def crossover(parents):
    parent1, parent2 = parents
    crossover_point = np.random.randint(1, len(parent1))
    child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
    return [child1, child2]


def mutate(offspring, mutation_rate):
    for child in offspring:
        for i in range(len(child)):
            if np.random.rand() < mutation_rate:
                child[i] = 1 - child[i]
    return offspring


def replace(population, offspring, fitnesses):
    elite_count = 2
    elite_indices = np.argsort(fitnesses)[-elite_count:]
    elite_indices1 = elite_indices.ravel().tolist()

    new_population = [population[i] for i in elite_indices1]
    new_population.extend(offspring)
    return new_population


components = [
    {'id': 1, 'defect_rate': 0.1, 'cost': 2, 'inspect_cost': 1},
    {'id': 2, 'defect_rate': 0.1, 'cost': 8, 'inspect_cost': 1},
    {'id': 3, 'defect_rate': 0.1, 'cost': 12, 'inspect_cost': 2},
    {'id': 4, 'defect_rate': 0.1, 'cost': 2, 'inspect_cost': 1},
    {'id': 5, 'defect_rate': 0.1, 'cost': 8, 'inspect_cost': 1},
    {'id': 6, 'defect_rate': 0.1, 'cost': 12, 'inspect_cost': 2},
    {'id': 7, 'defect_rate': 0.1, 'cost': 8, 'inspect_cost': 1},
    {'id': 8, 'defect_rate': 0.1, 'cost': 12, 'inspect_cost': 2}
]

subassemblies = [
    {'id': 1, 'defect_rate': 0.1, 'assembly_cost': 8, 'inspect_cost': 4, 'disassemble_cost': 6},
    {'id': 2, 'defect_rate': 0.1, 'assembly_cost': 8, 'inspect_cost': 4, 'disassemble_cost': 6},
    {'id': 3, 'defect_rate': 0.1, 'assembly_cost': 8, 'inspect_cost': 4, 'disassemble_cost': 6}
]

product = {
    'defect_rate': 0.1,
    'assembly_cost': 8,
    'inspect_cost': 6,
    'disassemble_cost': 10,
    'sale_price': 200,
    'replacement_loss': 40
}

best_decision, best_fitness, best_profit = genetic_algorithm(components, subassemblies, product)