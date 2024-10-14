import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\问题一示例数据.xlsx')
concentrations = data.iloc[:, 1].values
ks_values = data.iloc[:, 2].values

# 拆分数据
red_data = ks_values[1:9]
yellow_data = ks_values[9:17]
blue_data = ks_values[17:25]


# 绘制数据点
plt.scatter(concentrations[1:9], red_data, color='red', label='Red')
plt.scatter(concentrations[9:17], yellow_data, color='yellow', label='Yellow')
plt.scatter(concentrations[17:25], blue_data, color='blue', label='Blue')

plt.xlabel('Concentration')
plt.ylabel('K/S Value (at wavelength 600)')
plt.legend()
plt.show()
