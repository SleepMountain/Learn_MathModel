import xlrd
import random


def read_xls_to_dict(file_path):
    workbook = xlrd.open_workbook(file_path)
    worksheet = workbook.sheet_by_index(0)


    data_list = []

    # 获取表头（列名）
    headers = worksheet.row_values(0)

    # 从第二行开始，读取数据并转换为字典
    for row_idx in range(1, worksheet.nrows):
        row_data = worksheet.row_values(row_idx)
        data_dict = dict(zip(headers, row_data))
        data_list.append(data_dict)

    return data_list


def group_personnel_by_origin(data):
    origin_groups = {}

    for person in data:
        origin = person['籍贯']

        if origin not in origin_groups:
            origin_groups[origin] = []

        origin_groups[origin].append(person)

    return origin_groups


def sort_groups_by_size(groups):
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_groups


def calculate_minimum_group_size(sorted_groups):
    minimum_sizes = {}

    for origin, group in sorted_groups:
        minimum_size = len(group) // 8
        minimum_sizes[origin] = minimum_size

    return minimum_sizes


def print_group_sizes_and_names(groups, minimum_sizes):
    for origin, group in groups:
        group_size = len(group)
        minimum_size = minimum_sizes[origin]

        # 计算队长候选人数
        candidate_count = sum(1 for person in group if person['队长候选'] == 1)

        print(f"籍贯：{origin}，人数：{group_size}，最少人数：{minimum_size}，队长候选人数：{candidate_count}")

        names = [person['姓名'] for person in group]
        names_str = ', '.join(names)
        print(names_str)

file_path =r"D:\桌面\竞赛\数模\暑假训练\progress1\B题附件（改）.xls"
data = read_xls_to_dict(file_path)
grouped_data = group_personnel_by_origin(data)
sorted_groups = sort_groups_by_size(grouped_data)
minimum_sizes = calculate_minimum_group_size(sorted_groups)
print_group_sizes_and_names(sorted_groups, minimum_sizes)

print("")

def summarize_captain_candidates_injured_players(data):
    captain_candidates = []
    injured_players = []

    for person in data:
        if person['队长候选'] == 1:
            captain_candidates.append(person['姓名'])
        if person['伤病'] == 1:
            injured_players.append(person['姓名'])

    return captain_candidates, injured_players

captain_candidates, injured_players = summarize_captain_candidates_injured_players(data)


print("候补队长:")
captain_candidates_count = len(captain_candidates)
captain_candidates_str = ", ".join(captain_candidates)
print(f"候补队长总数：{captain_candidates_count}")
print(captain_candidates_str)

print("\n伤病人员:")
injured_players_count = len(injured_players)
injured_players_str = ", ".join(injured_players)
print(f"伤病人员总数：{injured_players_count}")
print(injured_players_str)

print("")

def calculate_average_age(data):
    total_age = 0
    for person in data:
        total_age += person['年龄']
    average_age = total_age / len(data)
    return average_age

def calculate_average_tenure(data):
    total_tenure = 0
    for person in data:
        total_tenure += person['入职年限']
    average_tenure = total_tenure / len(data)
    return average_tenure

average_age = calculate_average_age(data)
average_tenure = calculate_average_tenure(data)

print(f"安保人员平均年龄：{average_age}")
print(f"安保人员平均入职年限：{average_tenure}")

# 随机选择16位队长并随机平均分配到8个区域
captain_candidates_random = random.sample(captain_candidates, 16)
random.shuffle(captain_candidates_random)

area_captains = {}

for i in range(8):
    area_captains[f"区域{i+1}"] = captain_candidates_random[i*2:(i+1)*2]

print("\n随机分配队长到各个区域：")
for area, captains in area_captains.items():
    captain_str = ", ".join(captains)
    print(f"{area}: {captain_str}")

# 随机选择8位伤病人员并随机平均分配到8个区域
injured_players_random = random.sample(injured_players, 8)
random.shuffle(injured_players_random)

area_injured_players = {}

for i in range(8):
    area_injured_players[f"区域{i+1}"] = injured_players_random[i]

print("\n随机分配伤病人员到各个区域：")
for area, players in area_injured_players.items():
    print(f"{area}: {players}")

# 将9位亲属随机分配到8个区域
people = ['陈华', '陈杰', '高锋', '高杰', '王福', '王华', '王龙', '张进', '张坤']
area_people = {}

for i in range(8):
    area_people[f"区域{i+1}"] = []

assigned_people = set()

while len(people) > 0:
    random_person = random.choice(people)
    people.remove(random_person)

    assigned_area = None
    while assigned_area is None:
        random_area = random.choice(list(area_people.keys()))

        if random_person.startswith("陈") and any(person.startswith("陈") for person in area_people[random_area]):
            continue
        elif random_person.startswith("高") and any(person.startswith("高") for person in area_people[random_area]):
            continue
        elif random_person.startswith("王") and (any(person.startswith("王福") for person in area_people[random_area])
                                                or any(person.startswith("王华") or person.startswith("王龙") for person in area_people[random_area])):
            continue
        elif random_person.startswith("张") and any(person.startswith("张") for person in area_people[random_area]):
            continue
        else:
            area_people[random_area].append(random_person)
            assigned_people.add(random_person)
            assigned_area = random_area

print("\n随机分配人员到各个区域：")
for area, people_list in area_people.items():
    people_names = ', '.join(people_list)
    print(f"{area}: {people_names}")

# 汇总各个区域已分配的队长、伤病人员和亲属
area_people_summary = {}

for area in range(1, 9):
    area_key = f"区域{area}"
    area_people_summary[area_key] = area_captains[area_key] + [area_injured_players[area_key]] + area_people[area_key]

# 打印各个区域已分配的人员
print("\n各个区域已分配的人员：")
for area, people in area_people_summary.items():
    print(f"{area}: {', '.join(people)}")

# 汇合未分配人员信息
unassigned_personnel = []
for person in data:
    assigned = False

    # 检查是否已分配到某个区域
    for area, people_list in area_people.items():
        if person['姓名'] in people_list:
            assigned = True
            break

    # 如果未分配，则添加到未分配人员列表中
    if not assigned:
        unassigned_personnel.append(person)

# 将未分配人员汇合到一起
unassigned_group = group_personnel_by_origin(unassigned_personnel)

# 打印未分配人员信息
print("\n未分配人员信息：")
for origin, group in unassigned_group.items():
    print(f"籍贯：{origin}")
    names = [person['姓名'] for person in group]
    names_str = ', '.join(names)
    print(names_str)

    # 创建一个字典，表示各个小区的人员列表
    area_people = {}

    for i in range(1, 9):
        area_people[f"区域{i}"] = []

    # 计算每个小区的人员数量上限
    max_people_per_area = len(unassigned_personnel) // 8

    # 将未分配的人员按照年龄、籍贯和入职年限进行排序
    sorted_unassigned_personnel = sorted(unassigned_personnel, key=lambda x: (x['年龄'], x['籍贯'], x['入职年限']))

    # 遍历未分配的人员，将他们依次加入到各个小区中
    for index, person in enumerate(sorted_unassigned_personnel):
        area = f"区域{index % 8 + 1}"  # 轮流分配到各个小区

        if len(area_people[area]) < max_people_per_area:
            area_people[area].append(person)

    # 打印各个小区的人员信息
    print("\n平均分配后各个小区的人员信息：")
    for area, people_list in area_people.items():
        print(f"{area}:")
        for person in people_list:
            print(f"{person['姓名']} - 年龄：{person['年龄']}，籍贯：{person['籍贯']}，入职年限：{person['入职年限']}")

