import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.rcParams['font.family'] = 'SimHei'


# 读取Excel表格数据，指定列名
df = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\\result7.xlsx', names=['编号', '成本', '色差'], header=None)

# 添加第三列Z轴数据
df['Z'] = np.random.uniform(6, 13, size=len(df))

# 提取X轴、Y轴和Z轴数据
x = df['成本']
y = df['色差']
z = df['Z']

# 创建3D图形对象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制散点图
ax.scatter(x, y, z)
ax.set_xlabel('成本')
ax.set_ylabel('色差')
ax.set_zlabel('数量')

plt.show()
