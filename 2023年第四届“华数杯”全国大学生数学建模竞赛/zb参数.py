import pandas as pd
import numpy as np

# 读取附件一的数据
data1 = pd.read_excel(r"D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件一.xlsx")
wavelength = data1['λ/nm'].values.astype(float)
Sx = data1['S(λ)x(λ)'].values.astype(float)
Sy = data1['S(λ)y(λ)'].values.astype(float)
Sz = data1['S(λ)z(λ)'].values.astype(float)


# 读取附件二的数据
data2 = pd.read_excel(r"D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二.xlsx")
ks_values = data2.iloc[1:, 2:].values.astype(float)

# 读取附件三的数据
data3 = pd.read_excel(r"D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件三.xlsx")
sample_ids = data3['样本'].values.astype(int)
r_values = data3.iloc[:, 1:].values.astype(float)

def calculate_color_parameters(x, y, z):
    X = 2 * np.sum(Sx * x * wavelength)
    Y = 2 * np.sum(Sy * y * wavelength)
    Z = 2 * np.sum(Sz * z * wavelength)

    delta = (X + 15 * Y + 3 * Z) / 100

    L = 116 * delta**(1/3) - 16 if delta > 0.008856 else 903.3 * Y / 100
    a = 500 * ((X / 94.83)**(1/3) - (Y / 100)**(1/3)) if delta > 0.008856 else 3893.5 * (X / 94.83 - Y / 100)
    b = 200 * ((Y / 100)**(1/3) - (Z / 107.38)**(1/3)) if delta > 0.008856 else 1557.4 * (Y / 100 - Z / 107.38)

    return L, a, b

def calculate_color_difference(L1, a1, b1, L2, a2, b2):
    delta_L = L2 - L1
    delta_a = a2 - a1
    delta_b = b2 - b1

    color_difference = np.sqrt(delta_L**2 + delta_a**2 + delta_b**2)

    return color_difference

# 计算样本的颜色参数和色差
n_samples = len(sample_ids)
color_parameters = np.zeros((n_samples, 3))
color_differences = np.zeros((n_samples, n_samples))

for i in range(n_samples):
    sample_id = sample_ids[i]
    r_sample = r_values[i]

    x = ks_values[0] * r_sample
    y = ks_values[8] * r_sample
    z = ks_values[16] * r_sample

    L, a, b = calculate_color_parameters(x, y, z)
    color_parameters[i] = L, a, b

    for j in range(i+1, n_samples):
        r_compare = r_values[j]
        x = ks_values[0] * r_compare
        y = ks_values[8] * r_compare
        z = ks_values[16] * r_compare

        L_compare, a_compare, b_compare = calculate_color_parameters(x, y, z)
        color_differences[i, j] = calculate_color_difference(L, a, b, L_compare, a_compare, b_compare)

# 寻找每个样本的最优方案
optimal_solutions = []

for i in range(n_samples):
    sample_id = sample_ids[i]
    L, a, b = color_parameters[i]

    solutions = []
    for j in range(i+1, n_samples):
        compare_sample_id = sample_ids[j]
        color_difference = color_differences[i, j]
        solutions.append((compare_sample_id, color_difference))

    sorted_solutions = sorted(solutions, key=lambda x: x[1])[:10]  # 取前10个最优方案
    optimal_solutions.append((sample_id, L, a, b, sorted_solutions))

# 保存结果到Excel
output_data = pd.DataFrame(optimal_solutions, columns=["样本编号", "L*", "a*", "b*", "最优方案"])
output_file = r"D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\output.xlsx"
output_data.to_excel(output_file, index=False)
