import numpy as np
from scipy.spatial import distance
from scipy.optimize import minimize


# 示例数据，实际应用中需要根据附件提供的数据进行替换
target_r_values = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1])
formula_r_values = np.random.rand(20, 16)  # 假设有20个不同的配方，每个配方有16个波长的R值
color_mother_prices = np.array([10, 20, 15])  # 色母粒单位克重价格
max_cost = 50  # 最大成本限制
num_best = 10  # 选择最优配方的个数

# 计算色差
def calculate_color_difference(target_r, formula_r):
    return distance.euclidean(target_r, formula_r)

# 目标函数：最小化色差，满足成本限制
def objective_function(weights):
    total_color_diff = 0
    total_cost = 0
    for i in range(len(formula_r_values)):
        color_diff = calculate_color_difference(target_r_values, formula_r_values[i])
        cost = np.dot(weights, color_mother_prices)  # 计算成本
        total_color_diff += color_diff
        total_cost += cost
    return total_color_diff + total_cost

# 约束条件：成本不超过最大成本限制
def cost_constraint(weights):
    cost = np.dot(weights, color_mother_prices)
    return max_cost - cost

# 初始权重猜测值
initial_weights = np.ones(len(color_mother_prices)) / len(color_mother_prices)

# 优化问题
constraints = [{'type': 'ineq', 'fun': cost_constraint}]
result = minimize(objective_function, initial_weights, constraints=constraints)

# 获取最优权重
optimal_weights = result.x

# 选择最优配方
best_formulas = []
for formula_r in formula_r_values:
    color_diff = calculate_color_difference(target_r_values, formula_r)
    cost = np.dot(optimal_weights, color_mother_prices)
    best_formulas.append((formula_r, color_diff, cost))
best_formulas.sort(key=lambda x: x[1])  # 根据色差排序
best_formulas = best_formulas[:num_best]  # 选择最优配方的个数

# 打印最优配方、色差和成本
for i, (formula_r, color_diff, cost) in enumerate(best_formulas):
    print(f"配方{i + 1}：")
    print("R值：", formula_r)
    print("色差：", color_diff)
    print("成本：", cost)
    print()
