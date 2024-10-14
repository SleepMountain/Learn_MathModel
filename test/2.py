import numpy as np
import pandas as pd

S_data = pd.read_excel('D:\桌面\竞赛\数模\\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\附件一.xlsx').values[1:, :] # 排除第一行和第一列
wavelengths = S_data[:, 0]
S = S_data[:, 1:]
print(S_data.shape)

