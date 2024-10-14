import pandas as pd

# 读取CSV文件
df = pd.read_csv(r"D:\桌面\LR_2.csv",encoding='utf-8')

# 删除空值占比达 70%及以上的数据列
threshold = len(df) * 0.7
df = df.dropna(thresh=threshold, axis=1)

# 将处理后的数据另存为文件“LR_3.csv”
df.to_csv(r"D:\桌面\LR_3.csv", encoding='utf-8', index=False)


num_columns = len(df.columns)
print(f"处理后数据的列数为: {num_columns}")

