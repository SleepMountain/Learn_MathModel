import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 生成正态分布数据
mu = 0   # 均值
sigma = 10  # 标准差
x = np.linspace(-5, 30, 1000)  # 生成一组x值
y = norm.pdf(x, mu, sigma)  # 计算对应的正态分布概率密度函数值

# 找到右侧递减的部分
right_index = np.argmax(y)  # 找到最大值的索引
x_right = x[right_index:]   # 取右侧部分x值
y_right = y[right_index:]   # 取右侧部分y值

# 绘制正态分布曲线
plt.plot(x_right, y_right, color='blue')
plt.fill_between(x_right, y_right, color='blue', alpha=0)



plt.xlabel('X')
plt.ylabel('Probability')

plt.show()
