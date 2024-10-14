import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
data = pd.read_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/data.xlsx")

# 提取所需的列
data = data[['dUPDATE_TIME', 'sNODE_NAME', 'iNODE_STATUS']]

# 过滤出图像处理工序的数据
image_processing_data = data[data['sNODE_NAME'] == '图像处理']

# 将iNODE_STATUS列中的2和5转换为0和1，分别表示不返工和返工
image_processing_data['iNODE_STATUS'] = image_processing_data['iNODE_STATUS'].map({2: 0, 5: 1})

# 根据日期进行分组，并计算每天返工案卷的总数和各工序返工案卷数
grouped_data = image_processing_data.groupby('dUPDATE_TIME').agg({'iNODE_STATUS': 'sum', 'sNODE_NAME': 'count'})


# 计算每个工序返工案卷数占当天返工案卷总数的百分比
grouped_data['Percentage'] = grouped_data['iNODE_STATUS'] / grouped_data['sNODE_NAME'] * 100

# 创建一个堆积面积图
plt.stackplot(grouped_data.index, grouped_data['Percentage'], labels=grouped_data.index)

# 设置图表标题和坐标轴标签
plt.title('Percentage of Rework Cases in Image Processing by Day')
plt.xlabel('Date')
plt.ylabel('Percentage')

# 添加图例
plt.legend(loc='upper left')

# 输出结果到新的Excel文件
grouped_data.to_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result8.xlsx")

# 显示图表
plt.show()