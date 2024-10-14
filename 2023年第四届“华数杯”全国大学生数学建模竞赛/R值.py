import pandas as pd

# 读取表格一的数据
df1 = pd.read_excel(r'D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\KS--R.xlsx')


# 计算R值
df2 = pd.DataFrame()
for column in df1.columns:
    K = df1[column]
    R = 2+K+0.25*K**2
    df2[column] = R

# 创建新的DataFrame并保存为Excel文件
df2.to_excel(r'D:\桌面\竞赛\数模\2023年第四届“华数杯”全国大学生数学建模竞赛\表格\R.xlsx', index=False)