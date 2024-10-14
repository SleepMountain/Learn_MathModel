import random
import numpy as np


# 小区1老保安和新保安列表
old_security = ["凌*涌", "许*龙", "茹*勇", "覃*才", "朱*杰", "阮*飞", "黄*均", "佘*红"]
new_security = ["肖*同", "张*贵", "马*鑫", "金*", "何*", "罗*新", "徐*相", "尉*", "陈*杰"]
# 队长列表
captains = ["许*龙", "朱*杰", "罗*新"]

# 设置景区地图区域数量
num_regions = 5

# 初始化信息素矩阵
pheromone = np.ones((num_regions,))

# 初始化保安数量和经验
num_guards = np.array([10, 15, 8, 12, 20])
experience = np.array([5, 7, 3, 6, 9])

# 按照入职年限和经验排序老保安和新保安
old_security = sorted(old_security, key=lambda x: (x.split("*")[0], experience[old_security.index(x)]) if x in old_security else (x.split("*")[0], 0), reverse=True)
new_security = sorted(new_security, key=lambda x: (x.split("*")[0], experience[new_security.index(x)]), reverse=True)


def select_security(s_type):
    """
    选择一个保安（老保安或新保安）
    """
    if s_type == "old":
        return old_security.pop(0)
    else:
        return new_security.pop(0)


def is_valid(security, shift):
    """
    判断保安在某一班次是否合法（满足排他性和公平性要求）
    """
    # 判断队长是否在同一班次
    if security in captains and any(schedule["队长"] == security for schedule in patrol_schedule):
        return False

    # 判断保安是否连续巡逻超过3天
    if security_records.get(security, 0) >= 3:
        return False

    # 判断保安是否总是在同一班次巡逻
    if any(schedule["保安"] == security for schedule in patrol_schedule[-2:]):
        return False

    return True


# 初始化巡逻安排
patrol_schedule = []

# 初始化保安的巡逻情况记录，如连续巡逻天数和巡逻班次安排
security_records = {}


# 班次列表
shifts = ["0-8", "8-16", "16-24"]

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
            # 计算选择概率（信息素浓度和经验对选择的影响）
            selection_prob = (pheromone[i] ** 2) * (experience[i] ** 3)
            selection_prob = np.random.dirichlet(np.ones(num_regions))
            chosen_region = np.random.choice(np.arange(num_regions), p=selection_prob)
            region_choices.append(chosen_region)

        # 更新信息素
        pheromone *= 0.5  # 信息素挥发
        for i in range(num_ants):
            pheromone[region_choices[i]] += 1.0 / (1 + i)  # 蚂蚁留下信息素

    # 按照班次顺序进行巡逻安排
    for shift in shifts:
        # 初始化当前班次的巡逻安排
        current_schedule = {"班次": shift, "保安": [], "队长": ""}

        # 选择老保安和新保安，需老保安搭配新保安
        old_security_personnel = select_security("old")
        new_security_personnel = select_security("new")

        # 随机选择队长
        captain = random.choice(captains)

        # 判断保安和队长的合法性，直到找到合适的保安和队长
        while not is_valid(old_security_personnel, shift) or not is_valid(new_security_personnel, shift) or captain in [
            schedule["队长"] for schedule in patrol_schedule]:
            old_security.append(old_security_personnel)
            new_security.append(new_security_personnel)
            random.shuffle(old_security)
            random.shuffle(new_security)
            old_security_personnel = select_security("old")
            new_security_personnel = select_security("new")
            captain = random.choice(captains)

        # 更新巡逻安排和保安记录
        current_schedule["保安"] = [old_security_personnel, new_security_personnel]
        current_schedule["队长"] = captain
        patrol_schedule.append(current_schedule)
        for s in current_schedule["保安"]:
            security_records[s] = security_records.get(s, 0) + 1

# 输出巡逻安排
for schedule in patrol_schedule:
    print(schedule)