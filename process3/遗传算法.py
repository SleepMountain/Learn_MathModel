import random

# 定义适应度函数（目标函数）
def fitness_function(individual):
    # 根据个体的基因计算适应度值
    fitness = sum(individual)  # 假设适应度函数为基因中所有元素的和
    return fitness


# 初始化种群
def initialize_population(population_size, chromosome_length):
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(chromosome_length)]  # 假设基因由 0 和 1 组成
        population.append(individual)
    return population

# 选择操作（轮盘赌选择）
def selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    selected_indices = random.choices(range(len(population)), probabilities, k=len(population)//2)
    selected_population = [population[i] for i in selected_indices]
    return selected_population

# 交叉操作（单点交叉）
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1)-1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# 变异操作（位翻转变异）
def mutation(individual, mutation_rate):
    mutated_individual = individual.copy()
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutated_individual[i] = 1 - mutated_individual[i]  # 假设进行位翻转操作
    return mutated_individual

# 遗传算法主函数
def genetic_algorithm(population_size, chromosome_length, generations, mutation_rate):
    population = initialize_population(population_size, chromosome_length)

    for _ in range(generations):
        fitness_values = [fitness_function(individual) for individual in population]
        selected_population = selection(population, fitness_values)

        next_population = []

        while len(next_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child1, child2 = crossover(parent1, parent2)
            mutated_child1 = mutation(child1, mutation_rate)
            mutated_child2 = mutation(child2, mutation_rate)
            next_population.extend([mutated_child1, mutated_child2])

        population = next_population

    best_individual = max(population, key=fitness_function)
    best_fitness = fitness_function(best_individual)
    return best_individual, best_fitness

# 设置参数并运行遗传算法
population_size = 50
chromosome_length = 10
generations = 100
mutation_rate = 0.1

best_individual, best_fitness = genetic_algorithm(population_size, chromosome_length, generations, mutation_rate)
print("最佳个体:", best_individual)
print("最佳适应度:", best_fitness)
