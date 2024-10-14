import numpy as np
import random
import pandas as pd
attachment1_data = pd.read_excel("D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件一.xlsx")
wavelengths = attachment1_data.iloc[:, 0].values
s_x = attachment1_data.iloc[:, 1].values
s_y = attachment1_data.iloc[:, 2].values
s_z = attachment1_data.iloc[:, 3].values
attachment2_data = pd.read_excel("D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二.xlsx")
k_s_values = attachment2_data.iloc[:, 2:].values
attachment3_data = pd.read_excel("D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件三.xlsx")
r_values = attachment3_data.iloc[:, 1:].values

def objective_function(x):
    num_samples = len(x)
    num_wavelengths = len(wavelengths)
    total_cost = np.sum(x)
    target1 = num_samples * total_cost
    k_s_total = np.zeros(num_wavelengths)
    for i in range(num_samples):
        k_s_total += k_s_values[i] * x[i]
    target2 = np.sum(k_s_total)
    return target1, target2
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
def mopso(num_particles, max_iterations):
    num_samples = r_values.shape[0]
    dimensions = r_values.shape[1]
    lower_bound = np.zeros(num_samples)
    upper_bound = np.ones(num_samples)
    swarm_size = (num_particles, num_samples)
    positions = np.random.uniform(low=lower_bound, high=upper_bound, size=swarm_size)
    velocities = np.zeros(swarm_size)
    pbest_positions = np.copy(positions)
    pbest_scores = np.full((num_particles, 2), np.inf)
    pareto_front = []
    for iteration in range(max_iterations):
        for i in range(num_particles):
            targets = objective_function(positions[i])
            if targets[0] < pbest_scores[i, 0] and targets[1] < pbest_scores[i, 1]:
                cielab_distances = [calculate_cielab_distance([s_x[j], s_y[j], s_z[j]], r_values[j]) for j in range(num_samples)]
                if max(cielab_distances) <= 1:
                    pbest_scores[i] = targets
                    pbest_positions[i] = positions[i]
                    pareto_front.append((targets, positions[i]))
        inertia_weight = 0.7
        cognitive_weight = 1.5
        social_weight = 1.5
        for i in range(num_particles):
            r1 = random.random()
            r2 = random.random()
            cognitive_component = cognitive_weight * r1 * (pbest_positions[i] - positions[i])
            social_component = social_weight * r2 * (np.array(pareto_front)[:, 1][random.randint(0, len(pareto_front) - 1)] - positions[i])
            velocities[i] = inertia_weight * velocities[i] + cognitive_component + social_component
            velocities[i] = np.clip(velocities[i], lower_bound, upper_bound)
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], lower_bound, upper_bound)
    return pareto_front
pareto_front = mopso(num_particles=50, max_iterations=100)
for pareto_solution in pareto_front:
    print("Minimum number of dyes:", pareto_solution[0][0])
    print("Total cost:", pareto_solution[0][1])
    print("Colorant proportions:", pareto_solution[1])