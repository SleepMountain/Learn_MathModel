import pandas as pd

# 读取LR_5.csv文件
df = pd.read_csv(r"D:\桌面\LR_5.csv",encoding='utf-8')

# 计算利润率
df['利润率'] = df['B001000000'] / df['B001100000']

# 计算资产负债率
df['资产负债率'] = df['A002000000'] / df['A001000000']

# 删除利润率、资产负债率不在[-300%，300%]范围内的行
df = df[(df['利润率'] >= -3) & (df['利润率'] <= 3) & (df['资产负债率'] >= -3) & (df['资产负债率'] <= 3)]


# 将处理后的数据另存为文件“LR_new.csv”
df.to_csv(r"D:\桌面\LR_new.csv", encoding='utf-8', index=False)

# 呈现处理后的数据行数、列数
num_rows = len(df)
num_columns = len(df.columns)
print(f"处理后数据的行数为: {num_rows}")
print(f"处理后数据的列数为: {num_columns}")

# 呈现前 5 个企业的利润率、资产负债率
top5 = df.head()
print("前 5 个企业的利润率、资产负债率:")
print(top5[['利润率', '资产负债率']])
