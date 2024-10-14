import numpy as np
import random


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

def fitness_function(decision, components, subassemblies, product):
    total_s = 0
    total_c = 0
    for i, comp in enumerate(components):
        if decision[i]:
            total_s += comp['cost'] * comp['defect_rate']
            total_c += comp['inspect_cost']
    fitness = total_s - total_c + abs(total_c) + 1
    return fitness

def selection(population, fitnesses):
    selected = random.choices(population, weights=fitnesses, k=2)
    return selected


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]  # 翻转基因
    return individual


def initialize_population(size, n_bits):
    return [random.choices([0, 1], k=n_bits) for _ in range(size)]


def genetic_algorithm(components, subassemblies, product, pop_size=50, generations=100):
    n_b = len(components)
    population = initialize_population(pop_size, n_b)

    best_fitnesses = []
    for generation in range(generations):
        fitnesses = [fitness_function(individual, components, subassemblies, product) for individual in population]
        best_individual = max(population, key=lambda ind: fitness_function(ind, components, subassemblies, product))
        best_fitness = fitness_function(best_individual, components, subassemblies, product)
        best_fitnesses.append(best_fitness)

        new_p = []

        for _ in range(pop_size // 2):
            parents = selection(population, fitnesses)
            offspring1, offspring2 = crossover(*parents)
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)
            new_p.extend([offspring1, offspring2])

        population = new_p

        print(f"Generation {generation + 1} Best Fitness: {best_fitness}")

    best_individual = max(population, key=lambda ind: fitness_function(ind, components, subassemblies, product))
    best_fitness = fitness_function(best_individual, components, subassemblies, product)

    print(f"Best fitness over generations: {best_fitnesses}")

    return best_individual, best_fitness, best_fitnesses


best_decision, best_fitness, best_fitnesses = genetic_algorithm(components, subassemblies, product)
print(f"Best decision: {best_decision}")
print(f"Best fitness: {best_fitness}")

def simulate_production(batch_size, decision, components, subassemblies, product):
    assembled_c = []
    assembled_s = []
    assembled_p = []
    defective_p = []
    defective_s = []
    defective_c = []

    component_inspection_cost = 0
    component_defect_cost = 0
    subassembly_inspection_cost = 0
    subassembly_defect_cost = 0
    product_inspection_cost = 0
    product_defect_cost = 0
    product_replacement_loss = 0
    total_product_sales = 0
    total_profit = 0

    for i, comp in enumerate(components):
        if decision[i]:
            # 检测零配件
            defects = int(batch_size * comp['defect_rate'])
            good = batch_size - defects
            assembled_c.extend([comp] * good)
            defective_c.extend([comp] * defects)
            component_inspection_cost += batch_size * comp['inspect_cost']
            component_defect_cost += defects * comp['cost']
        else:
            assembled_c.extend([comp] * batch_size)

    for i in range(batch_size // 3):
        if len(assembled_c) >= 3:
            subassembly = assembled_c[:3]
            assembled_c = assembled_c[3:]
            inspect = np.random.rand() < subassemblies[0]['inspect_cost'] / (subassemblies[0]['inspect_cost'] + subassemblies[0]['defect_rate'] * subassemblies[0]['disassemble_cost'])
            if inspect and np.random.rand() < (1 - subassemblies[0]['defect_rate']):
                assembled_s.append(subassembly)
                subassembly_inspection_cost += subassemblies[0]['inspect_cost']
            elif not inspect and np.random.rand() < (1 - subassemblies[0]['defect_rate']):
                assembled_s.append(subassembly)
            else:
                defective_s.append(subassembly)
                subassembly_defect_cost += subassemblies[0]['disassemble_cost']

    for i in range(batch_size // 3):
        if len(assembled_s) >= 3:
            product = assembled_s[:3]
            assembled_s = assembled_s[3:]
            inspect = np.random.rand() < 6 / (
                        6 + 0.1 * 10)
            if inspect and np.random.rand() < 0.9:
                assembled_p.append(product)
                product_inspection_cost += 6
            elif not inspect and np.random.rand() < 0.9:
                assembled_p.append(product)
            else:
                defective_p.append(product)
                product_defect_cost += 10
                product_replacement_loss += 40

    total_product_sales = len(assembled_p) * 200

    total_profit = total_product_sales - (
        component_inspection_cost + component_defect_cost +
        subassembly_inspection_cost + subassembly_defect_cost +
        product_inspection_cost + product_defect_cost + product_replacement_loss
    )

    print("\n模拟结果:")
    print(f"组装组件总数: {len(assembled_c)}")
    print(f"装配的子装配体总数: {len(assembled_s)}")
    print(f"组装产品总数: {len(assembled_p)}")
    print(f"残次品: {len(defective_p)}")
    print(f"总销售金额: {total_product_sales}")
    print(f"总利润: {total_profit}")

    for i, comp in enumerate(components):
        print(
            f"零配件 {i + 1} 是否检测: {decision[i]}, 预期节省成本: {comp['cost'] * comp['defect_rate']}, 检测成本: {comp['inspect_cost']}")

    for i, subass in enumerate(subassemblies):
        print(
            f"半成品 {i + 1} 是否检测: {np.random.rand() < subass['inspect_cost'] / (subass['inspect_cost'] + subass['defect_rate'] * subass['disassemble_cost'])}, "
            f"预期节省成本: {subass['assembly_cost'] * subass['defect_rate']}, 检测成本: {subass['inspect_cost']}, 重装成本: {subass['disassemble_cost']}")

    print(
        f"成品是否检测: {np.random.rand() < 6 /( 6 + 0.1 * 10)}, "
        f"预期节省成本: {8 * 0.1}, 检测成本: {6}, 重装成本: {10}"
    )

batch_size = 1000

simulate_production(batch_size, best_decision, components, subassemblies, product)
