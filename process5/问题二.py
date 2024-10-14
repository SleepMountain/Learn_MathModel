import csv

def read_production_times(filename):
    production_times = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            production_times.append([int(time) for time in row])
    return production_times


def calculate_production_time(production_times):
    # 按照生产时间对工位进行排序
    sorted_positions = sorted(range(len(production_times)), key=lambda k: production_times[k])

    # 初始化每个工位的完成时间，并记录总生产时间
    finish_times = [0] * len(production_times)
    total_production_time = 0

    # 遍历每个疫苗类型
    for vaccine_type in range(10):
        # 获取当前可用的最短时间的工位
        current_position = sorted_positions.pop(0)

        # 计算当前疫苗类型在该工位的完成时间
        finish_times[current_position] += production_times[current_position][vaccine_type]

        # 更新总生产时间
        total_production_time = max(total_production_time, finish_times[current_position])

        # 将当前工位重新放回排序列表中
        sorted_positions.append(current_position)
        sorted_positions.sort(key=lambda k: finish_times[k])

    return total_production_time

# 从CSV文件中读取表一的数据
filename = 'table1.csv'
production_times = read_production_times(filename)

# 计算总生产时间
total_time = calculate_production_time(production_times)

print("总生产时间：", total_time)
