import math

# 定义每个工序的车间数量和耗时
workshops = {'a': 3, 'b': 8, 'c': 5}
time_required = {'a': 60, 'b': 120, 'c': 90}


# 计算每个工序的总时间
total_time_required = sum(time_required.values())

# 计算每个工序需要的车间数量
total_workshops = sum(workshops.values())

# 计算单位时间内可以完成的工序数量
processing_rate = total_workshops / total_time_required

# 计算待检修动车组的总数量
total_trains = math.ceil(12 * 60 / 15)

# 计算完成所有检修需要的总时间
total_time = total_trains / processing_rate

# 定义检修方案
repair_schedule = []

# 根据总时间和工序耗时安排具体检修方案
for i in range(total_trains):
    # 计算当前动车组进入检修的起始时间和结束时间
    start_time = i * 15
    end_time = start_time + total_time_required

    # 计算当前动车组在每个工序的具体检修时间
    a_end_time = start_time + time_required['a']
    b_start_time = a_end_time
    b_end_time = b_start_time + time_required['b']
    c_start_time = b_end_time
    c_end_time = c_start_time + time_required['c']

    # 添加当前动车组的检修时间段和使用的车间到检修方案中
    repair_schedule.append((start_time, a_end_time, ['a1', 'a2', 'a3'], 'a'))
    repair_schedule.append((b_start_time, b_end_time, ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'], 'b'))
    repair_schedule.append((c_start_time, c_end_time, ['c1', 'c2', 'c3', 'c4', 'c5'], 'c'))

# 打印结果
print("检修方案：")
for i, (start_time, end_time, workshops, process) in enumerate(repair_schedule):
    print("动车组", i//3 + 1, "检修时间段：", start_time, "-", end_time)
    print("所在工序：", process)
