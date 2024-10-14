import numpy as np
import pandas as pd

def normal_sampling(mean, std_dev, size=1):
    return np.random.normal(loc=mean, scale=std_dev, size=size)


def fitness_function(decision, components, subassemblies, product):
    total_savings = 0
    total_cost = 0
    total_inspection = 0
    total_defect = 0

    for i, comp in enumerate(components):
        sampled_defect_rate = max(0, normal_sampling(comp['defect_rate'], comp['defect_rate'] * 0.1))
        if decision[i]:
            total_savings += comp['cost'] * sampled_defect_rate
            total_cost += comp['inspect_cost']
            total_inspection += 1
        else:
            total_cost += comp['cost'] * sampled_defect_rate
            total_defect += 1

    subassembly_start = len(components)
    for j, subass in enumerate(subassemblies):
        sampled_defect_rate = max(0, normal_sampling(subass['defect_rate'], subass['defect_rate'] * 0.1))
        inspect_cost = subass['inspect_cost']
        defect_cost = subass['assembly_cost'] * sampled_defect_rate
        disassemble_cost = subass['disassemble_cost']

        if decision[subassembly_start + j]:
            total_savings += defect_cost
            total_cost += inspect_cost
            total_inspection += 1
        else:
            total_cost += defect_cost
            total_defect += 1

    product_start = subassembly_start + len(subassemblies)
    sampled_defect_rate = max(0, normal_sampling(product['defect_rate'], product['defect_rate'] * 0.1))
    inspect_cost = product['inspect_cost']
    defect_cost = product['assembly_cost'] * sampled_defect_rate
    disassemble_cost = product['disassemble_cost']

    if decision[product_start]:
        total_savings += defect_cost
        total_cost += inspect_cost
        total_inspection += 1
    else:
        total_cost += defect_cost
        total_defect += 1

    profit = product['sale_price'] - total_cost - product['replacement_loss'] + total_savings
    fitness = total_savings - total_cost + abs(total_cost)
    return fitness, profit, total_inspection, total_defect

def genetic_algorithm(components, subassemblies, product, population_size=50, generations=100, mutation_rate=0.01):
    decision_length = len(components) + len(subassemblies) + 1
    population = [np.random.choice([0, 1], decision_length) for _ in range(population_size)]

    best_decisions = []
    best_fitnesses = []
    best_profits = []

    for generation in range(generations):
        fitnesses_and_profits = [fitness_function(individual, components, subassemblies, product) for individual in population]
        fitnesses = [fit[0] for fit in fitnesses_and_profits]
        profits = [profit for _, profit, _, _ in fitnesses_and_profits]

        parents = selection(population, fitnesses)
        offspring = crossover(parents)
        mutated_offspring = mutate(offspring, mutation_rate)
        population = replace(population, mutated_offspring, fitnesses)

        best_individual = max(population, key=lambda ind: fitness_function(ind, components, subassemblies, product)[0])
        best_fitness, best_profit, best_inspection, best_defect = fitness_function(best_individual, components, subassemblies, product)
        best_decisions.append(best_individual)
        best_fitnesses.append(best_fitness)
        best_profits.append(best_profit)

    final_best_individual = max(best_decisions, key=lambda ind: fitness_function(ind, components, subassemblies, product)[0])
    final_best_fitness, final_best_profit, final_best_inspection, final_best_defect = fitness_function(final_best_individual, components, subassemblies, product)

    return final_best_individual, final_best_fitness, final_best_profit

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

def run_genetic_algorithm_multiple_times(components, subassemblies, product, runs=1000):
    results = []

    for run in range(runs):
        best_decision, best_fitness, best_profit = genetic_algorithm(components, subassemblies, product)
        results.append({
            'Run': run + 1,
            'Best Decision': best_decision,
            'Best Fitness': best_fitness,
            'Best Profit': best_profit
        })

    df = pd.DataFrame(results)
    df.to_excel('D:\桌面\问题四针对问题三1.xlsx', index=False)

run_genetic_algorithm_multiple_times(components, subassemblies, product)