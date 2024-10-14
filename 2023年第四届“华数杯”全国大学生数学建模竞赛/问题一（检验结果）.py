import pandas as pd
import numpy as np

# 读取附件二的数据
data = pd.read_excel(r'D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二.xlsx', skiprows=1)

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
        equation = f'K/S({wavelength}nm) = {round(coeff[0], 4)} * c^2 + {round(coeff[1], 4)} * c + {round(coeff[2], 4)}'
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

# 创建用于保存检验结果的DataFrame
output_data = pd.DataFrame()

# 将结果写入DataFrame
for result in results:
    colorant = result['colorant']
    for item in result['results']:
        wavelength = item['wavelength']
        coefficients = item['coefficients']
        rmse = item['RMSE']
        r_squared = item['R-squared']

        # 添加一行结果到DataFrame
        output_data = pd.concat([output_data, pd.DataFrame({
            '着色剂': [colorant],
            '波长': [wavelength],
            '拟合系数': [np.round(coefficients, 4)],
            '均方根误差（RMSE）': [round(rmse, 4)],
            '决定系数（R-squared）': [round(r_squared, 4)]
        })], ignore_index=True)

# 创建Excel文件并保存检验结果
output_path = r'D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\检验结果.xlsx'
output_data.to_excel(output_path, index=False)
print(f'检验结果已保存至 {output_path} 文件中。')
