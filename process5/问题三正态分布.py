import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 正态分布的参数
mu = 22.5  # 均值
sigma = 7.5  # 标准差
x_value = 30  # x轴值

# 生成x轴数据
x = np.linspace(0, 45, 100)


# 生成正态分布曲线上的y轴数据
y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

# 绘制曲线
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('Normal Distribution')
plt.grid(True)

# 计算红线右侧面积
cdf = norm.cdf(x_value, mu, sigma)
area_right = 1 - cdf

# 填充红线右侧面积
plt.fill_between(x, y, where=x >= x_value, color='red', alpha=0.3)

# 显示面积比例
plt.text(20, 0.04, f'Right Area Ratio: {area_right:.2f}', fontsize=12, ha='center')

# 在x轴为30的地方绘制竖线
plt.axvline(x=x_value, color='r', linestyle='--')

# 显示图形
plt.show()
