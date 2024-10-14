import pandas as pd

# 读取CSV文件
df = pd.read_csv("D:\桌面\LR_3.csv",encoding='utf-8')

# 删除包含空值的行
df = df.dropna()

# 将处理后的数据另存为文件“LR_4.csv”
df.to_csv("D:\桌面\LR_4.csv", encoding='utf-8', index=False)


# 在报告中呈现处理后数据的行数
num_rows = len(df)
print(f"处理后数据的行数为: {num_rows}")
