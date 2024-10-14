import pandas as pd
import numpy as np
import random

# 读取附件1中的光谱三刺激值加权表
attachment1 = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件一.xlsx', header=0)
wavelengths = attachment1['λ/nm']
sx = attachment1['S(λ)x(λ)']
sy = attachment1['S(λ)y(λ)']
sz = attachment1['S(λ)z(λ)']

# 读取附件2中的着色剂K/S基础数据库
attachment2 = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二问题三.xlsx', header=0)
dye_names = attachment2.iloc[:, 0]
dye_ks_values = attachment2.iloc[:, 1:]

# 读取附件3中的样本R值
attachment3 = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件三.xlsx', header=0)
sample_numbers = attachment3.iloc[:, 0]
r_values = attachment3.iloc[:, 1:]


# 定义遗传算法相关参数
population_size = 100  # 种群大小
generations = 50  # 迭代次数
mutation_rate = 0.02  # 变异率


# 光学模型计算XYZ值
def calculate_xyz(r, k_values):
    x_values = np.sum(sx * r * k_values)
    y_values = np.sum(sy * r * k_values)
    z_values = np.sum(sz * r * k_values)
    return x_values, y_values, z_values


# 计算CIELAB色差
def calculate_cielab_distance(target_xyz, dye_xyz):
    if target_xyz[0] / 94.83 > 0.008856 and target_xyz[1] / 94.83 > 0.008856 and target_xyz[2] / 94.83 > 0.008856:
        L = 116 * ((target_xyz[1] / 100) ** (1 / 3) - (dye_xyz[1] / 100) ** (1 / 3))-116 * ((dye_xyz[1] / 100) ** (1 / 3) - (dye_xyz[1] / 100) ** (1 / 3))
        a = 500 * ((target_xyz[0] /94.83)** (1 / 3) - (target_xyz[1] / 100) ** (1 / 3))-500 * ((dye_xyz[0] /94.83)** (1 / 3) - (dye_xyz[1] / 100) ** (1 / 3))
        b = 200 * ((target_xyz[1] / 100) ** (1 / 3) - (target_xyz[2] /107.38) ** (1 / 3))-200 * ((dye_xyz[1] / 100) ** (1 / 3) - (dye_xyz[2] /107.38) ** (1 / 3))
    else:
        L = 903.3 * ((target_xyz[1] / 100) ** (1 / 3) - (dye_xyz[1] / 100) ** (1 / 3)) - 903.3 * ((dye_xyz[1] / 100) ** (1 / 3) - (dye_xyz[1] / 100) ** (1 / 3))
        a = 3893.5 * ((target_xyz[0] / 94.83) ** (1 / 3) - (target_xyz[1] / 100) ** (1 / 3)) - 3893.5 * ( (dye_xyz[0] / 94.83) ** (1 / 3) - (dye_xyz[1] / 100) ** (1 / 3))
        b = 1557.4 * ((target_xyz[1] / 100) ** (1 / 3) - (target_xyz[2] / 107.38) ** (1 / 3)) - 1557.4 * ((dye_xyz[1] / 100) ** (1 / 3) - (dye_xyz[2] / 107.38) ** (1 / 3))
    return np.sqrt(a ** 2 + b ** 2 + L ** 2)


# 初始化种群
def initialize_population():
    population = []
    for _ in range(population_size):
        chromosome = random.choices(range(len(dye_names)), k = 10)
        population.append(chromosome)
    return population


# 评估适应度函数（计算总色差）
def evaluate_fitness(chromosome):
    total_distance = 0
    for sample_index in range(len(sample_numbers)):
        target_r = r_values.iloc[sample_index, :]
        target_xyz = calculate_xyz(target_r, dye_ks_values.iloc[:, 1])

        dye_xyz_list = []
        for dye_index in chromosome:
            dye_r = dye_ks_values.iloc[dye_index, 1]
            dye_xyz = calculate_xyz(dye_r, dye_ks_values.iloc[:, 1])
            dye_xyz_list.append(dye_xyz)

        distance_list = []
        for dye_xyz in dye_xyz_list:
            distance = calculate_cielab_distance(target_xyz, dye_xyz)
            distance_list.append(distance)

        min_distance = min(distance_list)
        total_distance += min_distance

    # 色差小于1的配方作为目标
    if min_distance <= 1:
        return total_distance
    else:
        return float('inf')


# 选择函数（锦标赛选择）
def selection(population, fitness_scores):
    selected_population = []
    while len(selected_population) < len(population):
        tournament_indices = random.choices(range(len(population)), k=5)
        tournament_fitness_scores = [fitness_scores[i] for i in tournament_indices]
        selected_index = tournament_indices[tournament_fitness_scores.index(min(tournament_fitness_scores))]
        selected_population.append(population[selected_index])
    return selected_population


# 交叉函数（两点交叉）
def crossover(parent1, parent2):
    crossover_point1 = random.randint(0, len(parent1) - 1)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1))
    child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]
    return child1, child2


# 变异函数（随机变异）
def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.randint(0, len(dye_names) - 1)
    return chromosome


# 执行遗传算法
def genetic_algorithm():
    population = initialize_population()
    best_fitness_score = float('inf')
    best_chromosomes = []

    for generation in range(generations):
        fitness_scores = []
        for chromosome in population:
            fitness_score = evaluate_fitness(chromosome)
            fitness_scores.append(fitness_score)

            if fitness_score < best_fitness_score:
                best_fitness_score = fitness_score
                best_chromosomes = [chromosome]
            elif fitness_score == best_fitness_score and chromosome not in best_chromosomes:
                best_chromosomes.append(chromosome)

        selected_population = selection(population, fitness_scores)

        next_population = []
        while len(next_population) < len(population):
            parent1, parent2 = random.choices(selected_population, k=2)
            child1, child2 = crossover(parent1, parent2)

            child1 = mutate(child1)
            child2 = mutate(child2)

            next_population.append(child1)
            next_population.append(child2)

        population = next_population

    # 输出最优配方及其对应的总色差
    for sample_index in range(len(sample_numbers)):
        target_r = r_values.iloc[sample_index, :]
        target_xyz = calculate_xyz(target_r, dye_ks_values.iloc[:, 1])

        print("样本编号：", sample_numbers.iloc[sample_index])
        best_chromosomes_sample = []
        best_fitness_score_sample = float('inf')

        for chromosome in best_chromosomes:
            dye_xyz_list = []
            for dye_index in chromosome:
                dye_r = dye_ks_values.iloc[dye_index, 1]
                dye_xyz = calculate_xyz(dye_r, dye_ks_values.iloc[:, 1])
                dye_xyz_list.append(dye_xyz)

            distance_list = []
            for dye_xyz in dye_xyz_list:
                distance = calculate_cielab_distance(target_xyz, dye_xyz)
                distance_list.append(distance)

            min_distance = min(distance_list)
            if min_distance < best_fitness_score_sample:
                best_fitness_score_sample = min_distance
                best_chromosomes_sample = [chromosome]
            elif min_distance == best_fitness_score_sample and chromosome not in best_chromosomes_sample:
                best_chromosomes_sample.append(chromosome)

        for i, best_chromosome in enumerate(best_chromosomes_sample):
            best_dye_names = [dye_names[j] for j in best_chromosome]
            print("第{}个最优配方：".format(i + 1), best_dye_names)
            print("总色差：", best_fitness_score_sample)


genetic_algorithm()
