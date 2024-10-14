import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel('D:\桌面\shuru.xlsx')  # 替换为实际的文件路径

# 提取数据列
numbers = df['Number']
hit_rate = df['Hit Rate']
linear_averages = df['Linear Averages']
averagers_rate = df['Averagers Rate']

# 创建图表
plt.figure(figsize=(10, 6))

# 绘制柱状图（只显示边框）
plt.bar(numbers, hit_rate, label='Hit Rate', color='blue', edgecolor='black', fill=False, hatch='', linewidth=2)


# 绘制平滑曲线并在每个点添加实心圆点
plt.plot(numbers, linear_averages, label='Linear Averages', color='red', marker='o', markersize=5, linestyle='-')
plt.scatter(numbers, linear_averages, color='red')  # 添加实心圆点

# 绘制虚线曲线
plt.plot(numbers, averagers_rate, label='Averagers Rate', color='green', linestyle='--')

# 设置图表标题和坐标轴标签
plt.xlabel('Number')
plt.ylabel('Rate (%)')

# 设置Y轴范围为0到100
plt.ylim(0, 1)

# 添加网格
plt.grid(True)

# 添加图例
plt.legend()

# 显示图表
plt.show()