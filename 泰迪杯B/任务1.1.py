import pandas as pd

# 读取CSV文件
df = pd.read_csv('D:\桌面\LR.csv', encoding='utf-8')

# 筛选字段"Typrep"值为"A"的数据
filtered_data = df[df['Typrep'] == 'A'][['Stkcd', 'Accper', 'Typrep', 'B001000000', 'B001100000', 'B001101000',
                                        'B001200000', 'B001201000', 'B001207000', 'B001209000', 'B001210000',
                                        'B001211000', 'B001212000', 'B001303000', 'B002300000']]


# 将筛选出的数据另存为文件"LR_1.csv"，文件编码设置为UTF-8
filtered_data.to_csv('D:\桌面\LR_1.csv', encoding='utf-8', index=False)

# 输出筛选后的数据行数、列数
num_rows, num_cols = filtered_data.shape
print(f"筛选后的数据行数: {num_rows}")
print(f"筛选后的数据列数: {num_cols}")
