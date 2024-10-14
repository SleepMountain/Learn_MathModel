import pandas as pd
import numpy as np
import random

file1 = pd.read_excel('D:\附件一.xlsx', header=0)
wavelengths = file1['λ/nm']
sx = file1['S(λ)x(λ)']
sy = file1['S(λ)y(λ)']
sz = file1['S(λ)z(λ)']
file2 = pd.read_excel('D:\附件二问题三.xlsx', header=0)
dye_names = file2.iloc[:, 0]
dye_ks_values = file2.iloc[:, 1:]
file3 = pd.read_excel('D:\附件三.xlsx', header=0)
Snumbers = file3.iloc[:, 0]
R = file3.iloc[:, 1:]
population_size = 100
generations = 50
mutation_rate = 0.02
def calculate_xyz(r, k_values):
    x = np.sum(sx * r * k_values)
    y = np.sum(sy * r * k_values)
    z = np.sum(sz * r * k_values)
    return x, y, z
def calculate_cielab_distance(T_xyz, d_xyz):
    if T_xyz[0] / 94.83 > 0.008856 and T_xyz[1] / 94.83 > 0.008856 and T_xyz[2] / 94.83 > 0.008856:
        L = 116 * ((T_xyz[1] / 100) ** (1 / 3) - (d_xyz[1] / 100) ** (1 / 3)) - 116 * ((d_xyz[1] / 100) ** (1 / 3) - (d_xyz[1] / 100) ** (1 / 3))
        a = 500 * ((T_xyz[0] / 94.83) ** (1 / 3) - (T_xyz[1] / 100) ** (1 / 3)) - 500 * ((d_xyz[0] / 94.83) ** (1 / 3) - (d_xyz[1] / 100) ** (1 / 3))
        b = 200 * ((T_xyz[1] / 100) ** (1 / 3) - (T_xyz[2] / 107.38) ** (1 / 3)) - 200 * ((d_xyz[1] / 100) ** (1 / 3) - (d_xyz[2] / 107.38) ** (1 / 3))
    else:
        L = 903.3 * ((T_xyz[1] / 100) ** (1 / 3) - (d_xyz[1] / 100) ** (1 / 3)) - 903.3 * ((d_xyz[1] / 100) ** (1 / 3) - (d_xyz[1] / 100) ** (1 / 3))
        a = 3893.5 * ((T_xyz[0] / 94.83) ** (1 / 3) - (T_xyz[1] / 100) ** (1 / 3)) - 3893.5 * ((d_xyz[0] / 94.83) ** (1 / 3) - (d_xyz[1] / 100) ** (1 / 3))
        b = 1557.4 * ((T_xyz[1] / 100) ** (1 / 3) - (T_xyz[2] / 107.38) ** (1 / 3)) - 1557.4 * ((d_xyz[1] / 100) ** (1 / 3) - (d_xyz[2] / 107.38) ** (1 / 3))
    return np.sqrt(a ** 2 + b ** 2 + L ** 2)
def initialize_population():
    pop = []
    for _ in range(population_size):
        chromosome = random.choices(range(len(dye_names)), k = 10)
        pop.append(chromosome)
    return pop
def evaluate_fitness(chromosome):
    allDistance = 0
    for Sindex in range(len(Snumbers)):
        TR = R.iloc[Sindex, :]
        Txyz = calculate_xyz(TR, dye_ks_values.iloc[:, 1])
        dye_xyz_list = []
        for dye_index in chromosome:
            dye_r = dye_ks_values.iloc[dye_index, 1]
            dye_xyz = calculate_xyz(dye_r, dye_ks_values.iloc[:, 1])
            dye_xyz_list.append(dye_xyz)
        distance_list = []
        for dye_xyz in dye_xyz_list:
            distance = calculate_cielab_distance(Txyz, dye_xyz)
            distance_list.append(distance)
        minDistance = min(distance_list)
        allDistance += minDistance
    if minDistance <= 1:
        return allDistance
    else:
        return float('inf')
def selection(population, fitness_scores):
    Spopulation = []
    while len(Spopulation) < len(population):
        tournamentIndices = random.choices(range(len(population)), k=5)
        tf = [fitness_scores[i] for i in tournamentIndices]
        seindex = tournamentIndices[tf.index(min(tf))]
        Spopulation.append(population[seindex])
    return Spopulation
def crossover(parent1, parent2):
    cpoint1 = random.randint(0, len(parent1) - 1)
    cpoint2 = random.randint(cpoint1 + 1, len(parent1))
    child1 = parent1[:cpoint1] + parent2[cpoint1:cpoint2] + parent1[cpoint2:]
    child2 = parent2[:cpoint1] + parent1[cpoint1:cpoint2] + parent2[cpoint2:]
    return child1, child2
def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.randint(0, len(dye_names) - 1)
    return chromosome
def genetic_algorithm():
    population = initialize_population()
    bfs = float('inf')
    bchromosomes = []
    for generation in range(generations):
        fscores = []
        for chromosome in population:
            fscore = evaluate_fitness(chromosome)
            fscores.append(fscore)
            if fscore < bfs:
                bfs = fscore
                bchromosomes = [chromosome]
            elif fscore == bfs and chromosome not in bchromosomes:
                bchromosomes.append(chromosome)
        selpopulation = selection(population, fscores)
        npopulation = []
        while len(npopulation) < len(population):
            parent1, parent2 = random.choices(selpopulation, k=2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            npopulation.append(child1)
            npopulation.append(child2)
        population = npopulation
    for samindex in range(len(Snumbers)):
        tar_r = R.iloc[samindex, :]
        tar_xyz = calculate_xyz(tar_r, dye_ks_values.iloc[:, 1])
        print("样本编号：", Snumbers.iloc[samindex])
        bestcs = []
        bestfss = float('inf')
        for chromosome in bchromosomes:
            dye_xyz_list = []
            for dye_index in chromosome:
                dye_r = dye_ks_values.iloc[dye_index, 1]
                dye_xyz = calculate_xyz(dye_r, dye_ks_values.iloc[:, 1])
                dye_xyz_list.append(dye_xyz)
            distance_list = []
            for dye_xyz in dye_xyz_list:
                distance = calculate_cielab_distance(tar_xyz, dye_xyz)
                distance_list.append(distance)
            mind = min(distance_list)
            if mind < bestfss:
                bestfss = mind
                bestcs = [chromosome]
            elif mind == bestfss and chromosome not in bestcs:
                bestcs.append(chromosome)
        for i, best_chromosome in enumerate(bestcs):
            best_dye_names = [dye_names[j] for j in best_chromosome]
            print("第{}个最优配方：".format(i + 1), best_dye_names)
            print("总色差：", bestfss)
genetic_algorithm()
