from datetime import datetime, timedelta

# 动车型号和工序所需时间字典
time_dict = {
    'CRH2': {'a': 60, 'b': 120, 'c': 90},
    'CRH3': {'a': 48, 'b': 144, 'c': 30},
    'CRH5': {'a': 78, 'b': 150, 'c': 90},
    'CRH6': {'a': 60, 'b': 162, 'c': 18}
}


# 工序车间字典
workshop_dict = {
    'a': ['a1', 'a2', 'a3'],
    'b': ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'],
    'c': ['c1', 'c2', 'c3', 'c4', 'c5']
}

# 初始化车间状态字典
workshop_status = {
    'a1': False, 'a2': False, 'a3': False,
    'b1': False, 'b2': False, 'b3': False, 'b4': False,
    'b5': False, 'b6': False, 'b7': False, 'b8': False,
    'c1': False, 'c2': False, 'c3': False, 'c4': False, 'c5': False
}

# 动车到达时间列表
arrival_times = [
    '00:16', '00:47', '01:22', '02:00', '02:21',
    '03:02', '03:31', '03:59', '04:01', '04:27', '05:09'
]

timeline = []  # 时间线上的记录

# 遍历每辆动车
for arrival_time in arrival_times:
    # 解析到达时间
    arrival_datetime = datetime.strptime(arrival_time, '%H:%M')
    car_timeline = []  # 每辆车的时间线记录

    # 遍历车型和对应工序时间
    for car_type, times in time_dict.items():
        # 遍历工序和时间
        for process, time in times.items():
            # 记录开始时间
            start_time = max(arrival_datetime, datetime.strptime(arrival_time, '%H:%M'))

            # 寻找可用的车间并更新车间状态
            workshop = None
            for w in workshop_dict[process]:
                if not workshop_status[w]:
                    workshop_status[w] = True
                    workshop = w
                    break

            # 计算结束时间
            end_time = start_time + timedelta(minutes=time)

            # 如果找不到可用车间，则在上一个车间等待
            if workshop is None:
                waiting_workshop = car_timeline[-1][-1]
                start_time = max(end_time, waiting_workshop[1] + timedelta(minutes=1))
                end_time = start_time + timedelta(minutes=time)

            # 记录该工序的时间段和车间
            car_timeline.append((start_time, end_time, workshop))

    # 将该辆车的时间线记录添加到总时间线上
    timeline.append((car_type, car_timeline))

# 按时间排序时间线记录
sorted_timeline = sorted(timeline, key=lambda x: x[1][0][0])

# 输出时间线记录
for car_type, car_timeline in sorted_timeline:
    print(f'{car_type}:')
    for start_time, end_time, workshop in car_timeline:
        print(f'{start_time.strftime("%H:%M")} - {end_time.strftime("%H:%M")}: {workshop} 车间')
    print()
