import numpy as np
import random
import pandas as pd

attachment1_data = pd.read_excel("D:\附件一.xlsx")
wavelengths = attachment1_data.iloc[:, 0].values
s_x = attachment1_data.iloc[:, 1].values
s_y = attachment1_data.iloc[:, 2].values
s_z = attachment1_data.iloc[:, 3].values
attachment2_data = pd.read_excel("D:\附件二.xlsx")
ks = attachment2_data.iloc[:, 2:].values
attachment3_data = pd.read_excel("D:\附件三.xlsx")
R = attachment3_data.iloc[:, 1:].values
def objective_function(x):
    Numsamples = len(x)
    Numwavelengths = len(wavelengths)
    tc = np.sum(x)
    t1 = Numsamples * tc
    kst = np.zeros(Numwavelengths)
    for i in range(Numsamples):
        kst += ks[i] * x[i]
    t2 = np.sum(kst)
    return t1, t2
def distance(T_xyz, D_xyz):
    if T_xyz[0] / 94.83 > 0.008856 and T_xyz[1] / 94.83 > 0.008856 and T_xyz[2] / 94.83 > 0.008856:
        L = 116 * ((T_xyz[1] / 100) ** (1 / 3) - (D_xyz[1] / 100) ** (1 / 3)) - 116 * ((D_xyz[1] / 100) ** (1 / 3) - (D_xyz[1] / 100) ** (1 / 3))
        a = 500 * ((T_xyz[0] / 94.83) ** (1 / 3) - (T_xyz[1] / 100) ** (1 / 3)) - 500 * ((D_xyz[0] / 94.83) ** (1 / 3) - (D_xyz[1] / 100) ** (1 / 3))
        b = 200 * ((T_xyz[1] / 100) ** (1 / 3) - (T_xyz[2] / 107.38) ** (1 / 3)) - 200 * ((D_xyz[1] / 100) ** (1 / 3) - (D_xyz[2] / 107.38) ** (1 / 3))
    else:
        L = 903.3 * ((T_xyz[1] / 100) ** (1 / 3) - (D_xyz[1] / 100) ** (1 / 3)) - 903.3 * ((D_xyz[1] / 100) ** (1 / 3) - (D_xyz[1] / 100) ** (1 / 3))
        a = 3893.5 * ((T_xyz[0] / 94.83) ** (1 / 3) - (T_xyz[1] / 100) ** (1 / 3)) - 3893.5 * ((D_xyz[0] / 94.83) ** (1 / 3) - (D_xyz[1] / 100) ** (1 / 3))
        b = 1557.4 * ((T_xyz[1] / 100) ** (1 / 3) - (T_xyz[2] / 107.38) ** (1 / 3)) - 1557.4 * ((D_xyz[1] / 100) ** (1 / 3) - (D_xyz[2] / 107.38) ** (1 / 3))
    return np.sqrt(a ** 2 + b ** 2 + L ** 2)
def mopso(numparticles, max):
    num_samples = R.shape[0]
    dimensions = R.shape[1]
    lower = np.zeros(num_samples)
    upper = np.ones(num_samples)
    size = (numparticles, num_samples)
    positions = np.random.uniform(low=lower, high=upper, size=size)
    velocities = np.zeros(size)
    pbestp = np.copy(positions)
    pbests = np.full((numparticles, 2), np.inf)
    paretof = []
    for iteration in range(max):
        for i in range(numparticles):
            targets = objective_function(positions[i])
            if targets[0] < pbests[i, 0] and targets[1] < pbests[i, 1]:
                cielab_distances = [distance([s_x[j], s_y[j], s_z[j]], R[j]) for j in range(num_samples)]
                if max(cielab_distances) <= 1:
                    pbests[i] = targets
                    pbestp[i] = positions[i]
                    paretof.append((targets, positions[i]))
        iweight = 0.7
        cweight = 1.5
        sweight = 1.5
        for i in range(numparticles):
            r1 = random.random()
            r2 = random.random()
            component = cweight * r1 * (pbestp[i] - positions[i])
            social_component = sweight * r2 * (np.array(paretof)[:, 1][random.randint(0, len(paretof) - 1)] - positions[i])
            velocities[i] = iweight * velocities[i] + component + social_component
            velocities[i] = np.clip(velocities[i], lower, upper)
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], lower, upper)
    return paretof
pareto_front = mopso(numparticles=50, max=100)
for pareto_solution in pareto_front:
    print("Minimum number of dyes:", pareto_solution[0][0])
    print("Total cost:", pareto_solution[0][1])
    print("Colorant proportions:", pareto_solution[1])
