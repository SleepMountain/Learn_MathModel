import pandas as pd

# 读取Excel数据
file_path = r'D:\桌面\result2.xlsx'
df = pd.read_excel(file_path)

# 将时间列转换为datetime格式
df['dUPDATE_TIME'] = pd.to_datetime(df['dUPDATE_TIME'])
df['dNODE_TIME'] = pd.to_datetime(df['dNODE_TIME'])

# 修改工序开始时间
df.loc[(df['dUPDATE_TIME'].dt.hour == 8) & (df['dUPDATE_TIME'].dt.minute >= 20) & (df['dUPDATE_TIME'].dt.minute < 30), 'dUPDATE_TIME'] = df['dUPDATE_TIME'] + pd.Timedelta(minutes=10)
df.loc[(df['dUPDATE_TIME'].dt.hour == 12) & (df['dUPDATE_TIME'].dt.minute >= 50) & (df['dUPDATE_TIME'].dt.minute < 60), 'dUPDATE_TIME'] = df['dUPDATE_TIME'].dt.floor('H') + pd.Timedelta(hours=13)

# 修改工序结束时间
df.loc[(df['dNODE_TIME'].dt.hour == 12) & (df['dNODE_TIME'].dt.minute >= 0) & (df['dNODE_TIME'].dt.minute < 30), 'dNODE_TIME'] = df['dNODE_TIME'].dt.floor('H')
df.loc[(df['dNODE_TIME'].dt.hour == 18) & (df['dNODE_TIME'].dt.minute >= 0) & (df['dNODE_TIME'].dt.minute < 10), 'dNODE_TIME'] = df['dNODE_TIME'].dt.floor('H')


# 将修改后的数据保存到新的Excel文件
output_file_path = r'D:\桌面\result3.xlsx'
df.to_excel(output_file_path, index=False)
