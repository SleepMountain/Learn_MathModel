import numpy as np
from scipy.optimize import curve_fit
import pandas as pd


# 示例数据，实际应用中需要根据附件提供的数据进行替换
wavelengths = np.array([400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700])
red_ks_data = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85])

# 非线性拟合函数
def fit_function(wavelength, a, b, c):
    return a * np.exp(b * wavelength) + c

# 初始猜测值
initial_guess = [1, -0.001, 0]

# 进行拟合
params, covariance = curve_fit(fit_function, wavelengths, red_ks_data, p0=initial_guess)

# 打印拟合参数
print("拟合参数:", params)

# 创建表格
columns = ['波长(nm)', '红色关系式', '红色拟合系数']
data = []

# 填充表格数据
for i in range(len(wavelengths)):
    row = [wavelengths[i], f'a * exp(b * {wavelengths[i]}) + c', params]
    data.append(row)

# 将数据转换为DataFrame并保存为表格
df = pd.DataFrame(data, columns=columns)
df.to_excel('拟合结果表格.xlsx', index=False)
