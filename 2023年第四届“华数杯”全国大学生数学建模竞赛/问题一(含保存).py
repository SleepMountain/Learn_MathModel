import pandas as pd
import numpy as np

# 读取附件二的数据
data = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件二.xlsx', skiprows=1)

# 着色剂名称和波长列表
colorants = ['红', '黄', '蓝']
wavelengths = np.arange(400, 701, 20)


# 创建空的DataFrame用于保存结果
result_data = pd.DataFrame()

# 循环处理每种着色剂
for i, colorant in enumerate(colorants):
    coeffs_list = []

    # 提取当前着色剂的K/S数据
    ks_data = data.iloc[i*8+1: (i+1)*8+1, 1:]
    concentrations = ks_data.iloc[:, 0].values
    ks_values = ks_data.iloc[:, 1:].values

    # 循环处理每个波长
    for j, wavelength in enumerate(wavelengths):
        coeff = np.polyfit(concentrations, ks_values[:, j], deg=2)
        coeffs_list.append(coeff)

        result_data.loc[f'K/S({wavelength}nm)', f'{colorant}着色剂'] = f'{coeff[0]:.6f} * c^2 + {coeff[1]:.6f} * c + {coeff[2]:.6f}'

    result_data[f'{colorant}着色剂拟合系数'] = coeffs_list

# 保存结果到Excel文件
save_path = r'D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\拟合结果.xlsx'
result_data.to_excel(save_path, index_label='波长')

print(f"拟合结果已保存到'{save_path}'文件中。")
