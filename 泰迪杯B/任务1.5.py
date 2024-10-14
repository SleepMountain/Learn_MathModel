import pandas as pd

# 读取CSV文件
df = pd.read_csv("D:\桌面\LR_4.csv", encoding='utf-8')

# 将字段“Accper”的日期数据转换为“YYYY-mm-dd”的格式
df['Accper'] = pd.to_datetime(df['Accper']).dt.strftime('%Y-%m-%d')

# 将处理后的数据另存为文件“LR_5.csv”
df.to_csv("D:\桌面\LR_5.csv", encoding='utf-8', index=False)

