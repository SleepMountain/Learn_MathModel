# 动态规划算法
def activity_selector(activities):


    activities.sort(key=lambda x: x[1])

    n = len(activities)
    c = [1] * n
    prev = [-1] * n  # 记录索引

    # 动态规划构建数组
    for i in range(1, n):
        for j in range(i):
            if activities[j][1] <= activities[i][0] and c[j] + 1 > c[i]:
                c[i] = c[j] + 1
                prev[i] = j

    # 回溯
    max_index = c.index(max(c))
    selected_activities = []
    while max_index != -1:
        selected_activities.append(activities[max_index])
        max_index = prev[max_index]
    selected_activities.reverse()

    return len(selected_activities), selected_activities

# 贪婪算法实现
def greedy_activity_selector(activities):

    activities.sort(key=lambda x: x[1])

    selected = [activities[0]]
    last_finish_time = activities[0][1]

    for start, finish in activities[1:]:
        if start >= last_finish_time:
            selected.append((start, finish))
            last_finish_time = finish

    return len(selected), selected



activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10)]

# 测试动态规划算法
dp_max_size, dp_max_set = activity_selector(activities)
print("动态规划算法结果:")
print(f"最大兼容活动集合的大小: {dp_max_size}")
print("最大兼容活动集合:", dp_max_set)

# 测试贪婪算法
greedy_max_size, greedy_max_set = greedy_activity_selector(activities)
print("\n贪婪算法结果:")
print(f"最大兼容活动集合的大小: {greedy_max_size}")
print("最大兼容活动集合:", greedy_max_set)