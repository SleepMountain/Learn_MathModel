import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\问题一示例数据.xlsx')
materials = data.iloc[:, 0].values
concentrations = data.iloc[:, 1].values
ks_values = data.iloc[:, 2].values

# 拆分数据
red_data = ks_values[1:9]
yellow_data = ks_values[9:17]
blue_data = ks_values[17:25]


# 多项式回归拟合
def polynomial_fit(x, y, degree):
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)
    return polynomial

red_polynomial = polynomial_fit(concentrations[1:9], red_data, 2)
yellow_polynomial = polynomial_fit(concentrations[9:17], yellow_data, 2)
blue_polynomial = polynomial_fit(concentrations[17:25], blue_data, 2)

# 绘制拟合曲线和数据点
x = np.linspace(min(concentrations[1:]), max(concentrations[1:]), 100)

plt.scatter(concentrations[1:9], red_data, color='red', label='Red')
plt.plot(x, red_polynomial(x), color='red')

plt.scatter(concentrations[9:17], yellow_data, color='yellow', label='Yellow')
plt.plot(x, yellow_polynomial(x), color='yellow')

plt.scatter(concentrations[17:25], blue_data, color='blue', label='Blue')
plt.plot(x, blue_polynomial(x), color='blue')

plt.xlabel('Concentration')
plt.ylabel('K/S Value (at wavelength 600)')
plt.legend()
plt.show()
