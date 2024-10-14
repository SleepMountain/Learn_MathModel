def calculate_time(arrival_time, car_type, inspection_level):
    workshop = {
        'a': ['a1', 'a2', 'a3'],
        'b': ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'],
        'c': ['c1', 'c2', 'c3', 'c4', 'c5'],
        'd': ['d1', 'd2', 'd3'],
        'e': ['e1', 'e2']
    }


    time = {
        'CRH2': {'a': 60, 'b': 120, 'c': 90, 'd': 240, 'e': 420},
        'CRH3': {'a': 48, 'b': 144, 'c': 30, 'd': 248, 'e': 390},
        'CRH5': {'a': 78, 'b': 150, 'c': 90, 'd': 180, 'e': 390},
        'CRH6': {'a': 60, 'b': 162, 'c': 18, 'd': 300, 'e': 420}
    }

    time_per_level = {
        'I': ['a', 'b'],
        'II': ['a', 'b', 'c'],
        'III': ['a', 'b', 'd'],
        'IV': ['a', 'b', 'd', 'e'],
        'V': ['a', 'b', 'c', 'd', 'e']
    }

    total_time = 0
    workshops_list = []

    for process in time_per_level[inspection_level]:
        process_time = time[car_type][process]

        # Find the first available workshop for the current process
        for workshop_name in workshop[process]:
            if workshop_name not in workshops_list:
                workshops_list.append(workshop_name)
                break

        total_time += process_time

    arrival_hour, arrival_minute = map(int, arrival_time.split(':'))
    completion_hour = arrival_hour + total_time // 60
    completion_minute = arrival_minute + total_time % 60

    return [[workshop_name, time] for workshop_name, time in
            zip(workshops_list, [total_time] * len(workshops_list))], f'{completion_hour:02d}:{completion_minute:02d}'


# 车辆到达时间表
arrivals = [
    ('00:16', 'CRH2', 'IV'),
    ('00:47', 'CRH5', 'II'),
    ('01:22', 'CRH2', 'II'),
    ('02:00', 'CRH6', 'I'),
    ('02:21', 'CRH3', 'III'),
    ('03:02', 'CRH6', 'II'),
    ('03:31', 'CRH2', 'V')
]

total_maintenance_time = 0

for arrival in arrivals:
    arrival_time, car_type, inspection_level = arrival
    workshops, completion_time = calculate_time(arrival_time, car_type, inspection_level)

    print(f'车辆类型：{car_type}，检验等级：{inspection_level}')
    print('经过的车间名称和时间：')
    for workshop in workshops:
        print(f'{workshop[0]} ')
    print(f'维修完成时间：{completion_time}\n')

    total_maintenance_time += int(completion_time.split(':')[0]) * 60 + int(completion_time.split(':')[1])
