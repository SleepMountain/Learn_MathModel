import numpy as np
import random

import openpyxl


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
        else:
            total_c += comp['cost'] * comp['defect_rate']

    for subass in subassemblies:
        inspect_cost = subass['inspect_cost']
        defect_cost = subass['assembly_cost'] * subass['defect_rate']
        disassemble_cost = subass['disassemble_cost']

        if np.random.rand() < inspect_cost / (inspect_cost + defect_cost * disassemble_cost):
            total_s += defect_cost
            total_c += inspect_cost
        else:
            total_c += defect_cost

    inspect_cost = product['inspect_cost']
    defect_cost = product['assembly_cost'] * product['defect_rate']
    disassemble_cost = product['disassemble_cost']

    if np.random.rand() < inspect_cost / (inspect_cost + defect_cost * disassemble_cost):
        total_s += defect_cost
        total_c += inspect_cost
    else:
        total_c += defect_cost


    fitness = total_s - total_c + abs(total_c)
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
    n_bits = len(components)
    population = initialize_population(pop_size, n_bits)

    best_fitnesses = []
    for generation in range(generations):
        fitnesses = [fitness_function(individual, components, subassemblies, product) for individual in population]
        best_individual = max(population, key=lambda ind: fitness_function(ind, components, subassemblies, product))
        best_fitness = fitness_function(best_individual, components, subassemblies, product)
        best_fitnesses.append(best_fitness)

        new_population = []

        for _ in range(pop_size // 2):
            parents = selection(population, fitnesses)
            offspring1, offspring2 = crossover(*parents)
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)
            new_population.extend([offspring1, offspring2])

        population = new_population

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

    component_i_c = 0
    component_d_c = 0
    subassembly_i_c = 0
    subassembly_d_c = 0
    product_i_c = 0
    product_d_c = 0
    product_r_loss = 0
    total_p_sales = 0
    total_p = 0

    for i, comp in enumerate(components):
        if decision[i]:
            defects = int(batch_size * comp['defect_rate'])
            good = batch_size - defects
            assembled_c.extend([comp] * good)
            defective_c.extend([comp] * defects)
            component_i_c += batch_size * comp['inspect_cost']
            component_d_c += defects * comp['cost']
        else:
            assembled_c.extend([comp] * batch_size)

    for i in range(batch_size // 3):
        if len(assembled_c) >= 3:
            subassembly = assembled_c[:3]
            assembled_c = assembled_c[3:]
            inspect = np.random.rand() < subassemblies[0]['inspect_cost'] / (subassemblies[0]['inspect_cost'] + subassemblies[0]['defect_rate'] * subassemblies[0]['disassemble_cost'])
            if inspect and np.random.rand() < (1 - subassemblies[0]['defect_rate']):
                assembled_s.append(subassembly)
                subassembly_i_c += subassemblies[0]['inspect_cost']
            elif not inspect and np.random.rand() < (1 - subassemblies[0]['defect_rate']):
                assembled_s.append(subassembly)
            else:
                defective_s.append(subassembly)
                subassembly_d_c += subassemblies[0]['disassemble_cost']

    for i in range(batch_size // 3):
        if len(assembled_s) >= 3:
            product = assembled_s[:3]
            assembled_s = assembled_s[3:]
            inspect = np.random.rand() < 6 / (6 + 0.1 * 10)
            if inspect and np.random.rand() < 0.9:
                assembled_p.append(product)
                product_i_c += 6
            elif not inspect and np.random.rand() < 0.9:
                assembled_p.append(product)
            else:
                defective_p.append(product)
                product_d_c += 10
                product_r_loss += 40

    total_p_sales = len(assembled_p) * 200

    total_p = total_p_sales - (
        component_i_c + component_d_c +
        subassembly_i_c + subassembly_d_c +
        product_i_c + product_d_c + product_r_loss
    )

    print("\n模拟结果:")
    print(f"组装组件总数: {len(assembled_c)}")
    print(f"装配的子装配体总数: {len(assembled_s)}")
    print(f"组装产品总数: {len(assembled_p)}")
    print(f"残次品: {len(defective_p)}")
    print(f"总销售金额: {total_p_sales}")
    print(f"总利润: {total_p}")

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

    results = {
        "assembled_components": len(assembled_c),
        "assembled_subassemblies": len(assembled_s),
        "assembled_products": len(assembled_p),
        "defective_products": len(defective_p),
        "total_product_sales": total_p_sales,
        "total_profit": total_p,
        "component_inspection_cost": component_i_c,
        "component_defect_cost": component_d_c,
        "subassembly_inspection_cost": subassembly_i_c,
        "subassembly_defect_cost": subassembly_d_c,
        "product_inspection_cost": product_i_c,
        "product_defect_cost": product_d_c,
        "product_replacement_loss": product_r_loss,
    }

    return results

best_decision, best_fitness, best_fitnesses = genetic_algorithm(components, subassemblies, product)
print(f"Best decision: {best_decision}")
print(f"Best fitness: {best_fitness}")

batch_size = 1000

iterations = 100

best_result = None
best_profit = float('-inf')

for _ in range(iterations):
    result = simulate_production(batch_size, best_decision, components, subassemblies, product)
    if result["total_profit"] > best_profit:
        best_profit = result["total_profit"]
        best_result = result

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Simulation Results10"

headers = [
    "Iteration", "Total Profit", "Total Product Sales", "Assembled Components",
    "Assembled Subassemblies", "Assembled Products", "Defective Products",
    "Component Decisions", "Subassembly Decisions", "Product Decision"
]
ws.append(headers)

best_result = None
best_profit = float('-inf')

for iteration in range(iterations):
    result = simulate_production(batch_size, best_decision, components, subassemblies, product)
    if result["total_profit"] > best_profit:
        best_profit = result["total_profit"]
        best_result = result

    component_decisions = [decision for decision in best_decision]
    subassembly_decisions = [np.random.rand() < subass['inspect_cost'] / (subass['inspect_cost'] + subass['defect_rate'] * subass['disassemble_cost']) for subass in subassemblies]
    product_decision = np.random.rand() < product['inspect_cost'] / (product['inspect_cost'] + product['defect_rate'] * product['disassemble_cost'])

    ws.append([
        iteration + 1,
        result["total_profit"],
        result["total_product_sales"],
        result["assembled_components"],
        result["assembled_subassemblies"],
        result["assembled_products"],
        result["defective_products"],
        str(component_decisions),
        str(subassembly_decisions),
        str(product_decision)
    ])

wb.save("D:\\桌面\\simulation_results10.xlsx")

print("\n最佳模拟结果:")
print(f"总利润: {best_result['total_profit']}")
print(f"总销售金额: {best_result['total_product_sales']}")
print(f"组装组件总数: {best_result['assembled_components']}")
print(f"装配的子装配体总数: {best_result['assembled_subassemblies']}")
print(f"组装产品总数: {best_result['assembled_products']}")
print(f"残次品: {best_result['defective_products']}")