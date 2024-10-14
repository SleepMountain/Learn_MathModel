import pandas as pd
import numpy as np

# 读取附件二的数据
data = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二.xlsx', skiprows=1)

# 着色剂名称和波长列表
colorants = ['红', '黄', '蓝']
wavelengths = np.arange(400, 701, 20)

# 用于存储每个着色剂在每个波长下的拟合系数和评价指标
results = []


# 循环处理每种着色剂
for i, colorant in enumerate(colorants):
    print(f'{colorant}着色剂的拟合关系式：')

    # 提取当前着色剂的K/S数据
    ks_data = data.iloc[i * 8 + 1: (i + 1) * 8 + 1, 1:]
    concentrations = ks_data.iloc[:, 0].values
    ks_values = ks_data.iloc[:, 1:].values

    # 用于存储每个波长下的拟合系数和评价指标
    colorant_results = []

    # 循环处理每个波长
    for j, wavelength in enumerate(wavelengths):
        coeff = np.polyfit(concentrations, ks_values[:, j], deg=2)
        equation = f'K/S({wavelength}nm) = {coeff[0]:.6f} * c^2 + {coeff[1]:.6f} * c + {coeff[2]:.6f}'
        print(equation)

        # 计算预测值
        predicted_values = np.polyval(coeff, concentrations)

        # 计算均方根误差（RMSE）
        rmse = np.sqrt(np.mean((predicted_values - ks_values[:, j]) ** 2))

        # 计算决定系数（R-squared）
        ss_total = np.sum((ks_values[:, j] - np.mean(ks_values[:, j])) ** 2)
        ss_residual = np.sum((ks_values[:, j] - predicted_values) ** 2)
        r_squared = 1 - ss_residual / ss_total

        # 存储拟合系数和评价指标
        colorant_results.append({
            'wavelength': wavelength,
            'equation': equation,
            'coefficients': coeff,
            'RMSE': rmse,
            'R-squared': r_squared
        })

    results.append({
        'colorant': colorant,
        'results': colorant_results
    })

    print()

# 输出检验结果
for result in results:
    print(f'{result["colorant"]}着色剂的检验结果：')
    for item in result['results']:
        print(f'波长{item["wavelength"]}nm:')
        print(f'拟合系数：{item["coefficients"]}')
        print(f'均方根误差（RMSE）：{item["RMSE"]:.6f}')
        print(f'决定系数（R-squared）：{item["R-squared"]:.6f}')
        print()
