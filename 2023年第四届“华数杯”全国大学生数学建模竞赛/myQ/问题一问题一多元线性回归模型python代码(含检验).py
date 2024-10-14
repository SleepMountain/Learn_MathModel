import pandas as pd
import numpy as np


data = pd.read_excel('D:\附件二.xlsx', skiprows=1)
colorants = ['红', '黄', '蓝']
wave = np.arange(400, 701, 20)
results = []
for i, color in enumerate(colorants):
    print(f'{color}着色剂的拟合关系式：')
    ks_data = data.iloc[i * 8 + 1: (i + 1) * 8 + 1, 1:]
    concent = ks_data.iloc[:, 0].values
    ks = ks_data.iloc[:, 1:].values
    color_r = []
    for j, wavelength in enumerate(wave):
        coeff = np.polyfit(concent, ks[:, j], deg=2)
        equation = f'K/S({wavelength}nm) = {coeff[0]:.6f} * c^2 + {coeff[1]:.6f} * c + {coeff[2]:.6f}'
        print(equation)
        preValues = np.polyval(coeff, concent)
        # 计算均方根误差
        rmse = np.sqrt(np.mean((preValues - ks[:, j]) ** 2))
        # 计算决定系数（R-squared）
        ss_total = np.sum((ks[:, j] - np.mean(ks[:, j])) ** 2)
        ss_residual = np.sum((ks[:, j] - preValues) ** 2)
        r_squared = 1 - ss_residual / ss_total
        color_r.append({
            'wavelength': wavelength,
            'equation': equation,
            'coefficients': coeff,
            'RMSE': rmse,
            'R-squared': r_squared
        })
    results.append({
        'colorant': color,
        'results': color_r
    })
    print()
for result in results:
    print(f'{result["colorant"]}着色剂的检验结果：')
    for item in result['results']:
        print(f'波长{item["wavelength"]}nm:')
        print(f'拟合系数：{item["coefficients"]}')
        print(f'均方根误差（RMSE）：{item["RMSE"]:.6f}')
        print(f'决定系数（R-squared）：{item["R-squared"]:.6f}')
        print()
