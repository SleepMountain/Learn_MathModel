import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimHei'


# 读取Excel表格数据，指定列名
df = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\\result2.xlsx', names=['编号', '成本', '色差'], header=None)

# 提取X轴和Y轴数据
x = df['成本']
y = df['色差']

# 绘制点图
plt.scatter(x, y)
plt.xlabel('成本')
plt.ylabel('色差')
plt.show()
