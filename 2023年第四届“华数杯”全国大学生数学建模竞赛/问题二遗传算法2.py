import pandas as pd
import numpy as np
from scipy.optimize import linprog

# 读取附件一数据
attachment1_data = pd.read_excel("D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件一.xlsx")
attachment1_data = attachment1_data.values[:, 1:]  # 去除第一列的序号

# 读取附件二数据
attachment2_data = pd.read_excel("D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二.xlsx")
attachment2_data = attachment2_data.values[:, 1:]  # 去除第一列的材料名称

# 读取附件三数据
attachment3_data = pd.read_excel("D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件三.xlsx")

# 循环处理每个目标样本
for i in range(10):
    # 提取目标样的R值
    target_R = attachment3_data.values[i, 1:]


    # 提取光谱三刺激值加权表
    weight_table = attachment1_data[:, 1:]

    # 提取着色剂K/S基础数据库
    K_S_database = attachment2_data[:, 1:]

    # 定义线性规划模型
    c = np.zeros(K_S_database.shape[0])
    A = np.zeros((K_S_database.shape[1], K_S_database.shape[0]))
    b = np.ones(K_S_database.shape[1])
    bounds = [(0, 1)] * K_S_database.shape[0]

    # 构建线性规划模型的约束矩阵和目标函数系数
    for j in range(K_S_database.shape[1]):
        A[j, :] = K_S_database[:, j] * weight_table[j, 0]

    # 定义优化目标为最小化色差的总和
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    # 计算所有配方的R值和色差
    all_R_values = np.dot(K_S_database.T, res.x) * weight_table[:, 0]
    all_color_diff = np.abs(target_R - all_R_values)

    # 构建包含配方索引和对应色差的列表
    recipe_diff_list = [(j, diff) for j, diff in enumerate(all_color_diff)]

    # 根据色差从小到大对配方进行排序
    sorted_recipes = sorted(recipe_diff_list, key=lambda x: x[1])

    # 筛选出色差小于1的前10个配方
    filtered_recipes = [recipe for recipe in sorted_recipes if recipe[1] < 1][:10]

    print("目标样本", i+1)
    print("-------------------------")
    # 输出色差最接近的10个不同配方
    for index, diff in filtered_recipes:
        recipe = K_S_database[index]
        print("配方索引：", index)
        print("配方的R值：", all_R_values[index])
        print("配方与目标样的色差：", diff)
        print("配方成分：", recipe)
        print("-------------------------")
