import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel表格数据
data = pd.read_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/data.xlsx")

# 筛选出图像处理工序的数据，并统计每个操作人员的返工案卷数
image_processing_data = data[data['sNODE_NAME'] == '图像处理']
rework_count = image_processing_data.groupby('iUSER_ID').apply(lambda x: x[x['iNODE_STATUS'] == 5]['iNODE_STATUS'].count())

# 计算返工案卷总数
total_rework = rework_count.sum()

# 计算每个操作人员返工案卷数占总数的百分比
percentage = rework_count / total_rework * 100

# 按百分比进行排序
sorted_data = pd.DataFrame({'操作人员': percentage.index, '返工案卷数': rework_count.values, '百分比': percentage.values})
sorted_data.sort_values('百分比', ascending=False, inplace=True)


# 合并排名第10位及以后的数据
other_percentage = sorted_data[9:]['百分比'].sum()
other_data = pd.DataFrame({'操作人员': ['其他'], '返工案卷数': [sorted_data[9:]['返工案卷数'].sum()], '百分比': [other_percentage]})
sorted_data = sorted_data[:9].append(other_data)

# 绘制饼图
plt.pie(sorted_data['百分比'], labels=sorted_data['操作人员'], autopct='%1.1f%%')
plt.title('操作人员返工案卷数占比')
plt.show()