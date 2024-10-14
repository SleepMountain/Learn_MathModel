import math
import openpyxl

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

# 创建一个新的Excel工作簿
workbook = openpyxl.Workbook()

# 获取默认的工作表
sheet = workbook.active

# 写入列名
sheet['A1'] = "动车组编号"
sheet['B1'] = "检修开始时间"
sheet['C1'] = "检修结束时间"
sheet['D1'] = "所在工序"

# 将检修方案写入Excel表格
for i, (start_time, end_time, workshops, process) in enumerate(repair_schedule):
    row = i + 2
    sheet[f'A{row}'] = i // 3 + 1  # 动车组编号
    sheet[f'B{row}'] = start_time  # 检修开始时间
    sheet[f'C{row}'] = end_time  # 检修结束时间
    sheet[f'D{row}'] = process  # 所在工序

# 保存Excel工作簿到指定目录下的文件
file_path = "D:\桌面\竞赛\数模\暑假训练\progress4\question1.xlsx"
workbook.save(file_path)

# 打印保存成功的消息
print("代码已保存到文件:", file_path)
