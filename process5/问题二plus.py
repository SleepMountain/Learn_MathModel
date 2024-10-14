import numpy as np
import pandas as pd

processing_times = {
    'MY1': [13, 14, 19, 11],
    'MY2': [98, 19, 17, 18],
    'MY3': [20, 15, 14, 15],
    'MY4': [7, 9, 15, 18],
    'MY5': [8, 13, 13, 11],
    'MY6': [19, 20, 14, 13],
    'MY7': [10, 16, 11, 18],
    'MY8': [16, 9, 17, 16],
    'MY9': [14, 12, 7, 8],
    'MY10': [12, 7, 9, 15]
}


# 计算每个工位的平均加工时间
avg_processing_times = {key: np.mean(value) for key, value in processing_times.items()}

# 按照工艺流程的顺序依次安排疫苗生产顺序
production_order = []
remaining_vaccines = 10  # 假设有10箱疫苗需要生产

while remaining_vaccines > 0:
    min_processing_time = float('inf')
    next_station = ''

    # 在剩余未安排生产的疫苗中选择平均加工时间最短的工位
    for station in avg_processing_times:
        if avg_processing_times[station] < min_processing_time and station not in production_order:
            min_processing_time = avg_processing_times[station]
            next_station = station

    production_order.append(next_station)
    remaining_vaccines -= 1

# 计算进入CJ1时刻和离开CJ4时刻
entry_time_CJ1 = 0
leave_time_CJ4 = 0

for i, station in enumerate(production_order):
    entry_time_CJ1 += avg_processing_times[station]
    leave_time_CJ4 = max(leave_time_CJ4, entry_time_CJ1)

# 将进入CJ1时刻和离开CJ4时刻转换为分钟表示
entry_time_CJ1_minutes = int(entry_time_CJ1 * 60)  # 转换为分钟
leave_time_CJ4_minutes = int(leave_time_CJ4 * 60)  # 转换为分钟

# 输出结果
df = pd.DataFrame({'加工顺序（填疫苗编号）': range(1, 11),
                   '进入CJ1时刻': pd.to_datetime([entry_time_CJ1_minutes], format='%H%M'),
                   '离开CJ4时刻': pd.to_datetime([leave_time_CJ4_minutes], format='%H%M')})

print(df)
