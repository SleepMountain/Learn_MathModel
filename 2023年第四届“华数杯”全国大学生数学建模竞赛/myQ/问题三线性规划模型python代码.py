import pandas as pd
import numpy as np
from pulp import *

data1 = pd.read_excel("D:\附件一.xlsx")
wave = data1['λ/nm'].values.astype(float)
Sx = data1['S(λ)x(λ)'].values.astype(float)
Sy = data1['S(λ)y(λ)'].values.astype(float)
Sz = data1['S(λ)z(λ)'].values.astype(float)
data2 = pd.read_excel("D:\附件二.xlsx")
ks_values = data2.iloc[1:, 2:].values.astype(float)
data3 = pd.read_excel("D:\附件三.xlsx")
Sids = data3['样本'].values.astype(int)
Rvalues = data3.iloc[:, 1:].values.astype(float)
def parameters(x, y, z):
    X = 2 * np.sum(Sx * x * wave)
    Y = 2 * np.sum(Sy * y * wave)
    Z = 2 * np.sum(Sz * z * wave)
    delta = (X + 15 * Y + 3 * Z) / 100
    L = 116 * delta**(1/3) - 16 if delta > 0.008856 else 903.3 * Y / 100
    a = 500 * ((X / 94.83)**(1/3) - (Y / 100)**(1/3)) if delta > 0.008856 else 3893.5 * (X / 94.83 - Y / 100)
    b = 200 * ((Y / 100)**(1/3) - (Z / 107.38)**(1/3)) if delta > 0.008856 else 1557.4 * (Y / 100 - Z / 107.38)
    return L, a, b
def difference(L1, a1, b1, L2, a2, b2):
    DL = L2 - L1
    DA = a2 - a1
    DB = b2 - b1
    Cdifference = np.sqrt(DL**2 + DA**2 + DB**2)
    return Cdifference
Nsamples = len(Sids)
cparameters = np.zeros((Nsamples, 3))
cdifferences = np.zeros((Nsamples, Nsamples))
for i in range(Nsamples):
    sample_id = Sids[i]
    r_sample = Rvalues[i]
    x = ks_values[sample_id-1] * r_sample
    y = ks_values[sample_id+5] * r_sample
    z = ks_values[sample_id+12] * r_sample
    L, a, b = parameters(x, y, z)
    cparameters[i] = L, a, b
    for j in range(i+1, Nsamples):
        compare_sample_id = Sids[j]
        r_compare = Rvalues[j]
        x = ks_values[compare_sample_id-1] * r_compare
        y = ks_values[compare_sample_id+5] * r_compare
        z = ks_values[compare_sample_id+12] * r_compare
        L_compare, a_compare, b_compare = parameters(x, y, z)
        cdifferences[i, j] = difference(L, a, b, L_compare, a_compare, b_compare)
tsi = 1
targetL, target_a, target_b = cparameters[tsi - 1]
problem = LpProblem("ColorMatching", LpMinimize)
ncolorants = 3
price_red = 60
price_yellow = 65
price_blue = 63
red = LpVariable("red", lowBound=0)
yellow = LpVariable("yellow", lowBound=0)
blue = LpVariable("blue", lowBound=0)
problem += price_red * red + price_yellow * yellow + price_blue * blue
problem += red + yellow + blue == 2000
for i in range(Nsamples):
    if i != tsi - 1:
        compare_L, compare_a, compare_b = cparameters[i]
        color_difference = difference(targetL, target_a, target_b, compare_L, compare_a, compare_b)
        problem += color_difference.item() <= 1
# 求解线性规划问题
status = problem.solve()
if status == 1:
    print("最优配方:")
    print(f"红色: {value(red):.2f} 克")
    print(f"黄色: {value(yellow):.2f} 克")
    print(f"蓝色: {value(blue):.2f} 克")
else:
    print("未找到最优解，请检查约束条件设置是否合理。")
