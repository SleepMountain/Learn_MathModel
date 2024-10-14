import numpy as np
import matplotlib.pyplot as plt


def least_squares(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    num = 0
    den = 0
    for i in range(len(x)):
        num += (x[i] - x_mean) * (y[i] - y_mean)
        den += (x[i] - x_mean) ** 2
    a = num / den
    b = y_mean - a * x_mean
    return a, b

x = [2, 2.5, 3, 4, 5, 5.5]
y = [4, 4.5, 6, 8, 8.5, 9]

a, b = least_squares(x, y)

# 绘制原始数据点
plt.scatter(x, y, label='点')

# 计算并绘制线性回归线
x_r = np.linspace(min(x), max(x), 100)
y_r = a * x_r + b
plt.plot(x_r, y_r, 'r', label='线')

plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()