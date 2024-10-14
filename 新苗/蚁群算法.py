import numpy as np

# 设置区域数量
num_regions = 5

# 初始化信息素矩阵
pheromone = np.ones((num_regions,))


# 初始化保安数量和经验
num_guards = np.array([10, 15, 8, 12, 20])
experience = np.array([5, 7, 3, 6, 9])

# 设置蚂蚁数量
num_ants = 5

# 设置迭代次数
num_iterations = 100

# 蚁群算法主循环
for iter in range(num_iterations):
    # 每只蚂蚁选择区域
    for ant in range(num_ants):
        region_choices = []
        for i in range(num_regions):
            # 计算选择概率
            selection_prob = (pheromone[i] ** 2) * (experience[i] ** 3)  # 假设信息素浓度和经验对选择的影响
            selection_prob = np.random.dirichlet(np.ones(num_regions))
            chosen_region = np.random.choice(np.arange(num_regions), p=selection_prob)
            region_choices.append(chosen_region)

        # 更新信息素
        pheromone *= 0.5  # 信息素挥发
        for i in range(num_ants):
            pheromone[region_choices[i]] += 1.0 / (1 + i)  # 蚂蚁留下信息素

    # 输出每次迭代后的信息素浓度
    print("Iteration", iter+1, ":", pheromone)
