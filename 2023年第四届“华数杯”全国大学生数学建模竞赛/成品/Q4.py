import numpy as np
from scipy.spatial import distance
from scipy.optimize import minimize


# 示例数据，实际应用中需要根据附件提供的数据进行替换
target_samples_r_values = np.random.rand(5, 16)  # 假设有5个目标样本，每个样本有16个波长的R值
formula_r_values = np.random.rand(30, 16)  # 假设有30个不同的配方，每个配方有16个波长的R值
color_mother_prices = np.array([10, 20, 15])  # 色母粒单位克重价格
max_cost = 50  # 最大成本限制
num_best_per_sample = 5  # 每个样本选取的最优配方数量

# 计算色差
def calculate_color_difference(target_r, formula_r):
    return distance.euclidean(target_r, formula_r)

# 目标函数：最小化色差，满足成本限制，尽量减少使用的色母粒数量
def objective_function(weights):
    total_color_diff = 0
    total_cost = 0
    num_used_color_mothers = np.sum(weights > 0)
    for i in range(len(formula_r_values)):
        color_diff = calculate_color_difference(target_r_values, formula_r_values[i])
        cost = np.dot(weights, color_mother_prices)
        total_color_diff += color_diff
        total_cost += cost
    return total_color_diff + total_cost + num_used_color_mothers

# 约束条件：成本不超过最大成本限制
def cost_constraint(weights):
    cost = np.dot(weights, color_mother_prices)
    return max_cost - cost

# 约束条件：每个样本选择的配方数量不超过指定数量
def num_formulas_constraint(weights):
    return np.sum(weights) - num_best_per_sample

# 初始权重猜测值
initial_weights = np.ones(len(color_mother_prices)) / len(color_mother_prices)

# 优化问题
constraints = [{'type': 'ineq', 'fun': cost_constraint},
               {'type': 'eq', 'fun': num_formulas_constraint}]
result = minimize(objective_function, initial_weights, constraints=constraints)

# 获取最优权重
optimal_weights = result.x

# 选择最优配方
best_formulas_per_sample = []
for target_r in target_samples_r_values:
    best_formulas = []
    for formula_r in formula_r_values:
        color_diff = calculate_color_difference(target_r, formula_r)
        cost = np.dot(optimal_weights, color_mother_prices)
        best_formulas.append((formula_r, color_diff, cost))
    best_formulas.sort(key=lambda x: x[1])
    best_formulas_per_sample.append(best_formulas[:num_best_per_sample])

# 打印每个样本的最优配方
for i, sample_formulas in enumerate(best_formulas_per_sample):
    print(f"样本{i + 1}的最优配方：")
    for j, (formula_r, color_diff, cost) in enumerate(sample_formulas):
        print(f"配方{j + 1}：")
        print("R值：", formula_r)
        print("色差：", color_diff)
        print("成本：", cost)
        print()
