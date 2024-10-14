import pandas as pd
import matplotlib.pyplot as plt

# 从 Excel 读取数据
file_path = r'D:\桌面\data.xlsx'  # 假设文件路径为 "D:\桌面\data.xlsx"，确保路径中的反斜杠使用了两个，或者使用单斜杠
df = pd.read_excel(file_path)

# 将时间字符串转换为 datetime 类型
df['dUPDATE_TIME'] = pd.to_datetime(df['dUPDATE_TIME'])
df['dNODE_TIME'] = pd.to_datetime(df['dNODE_TIME'])

# 提取具体时间并转换为字符串格式
df['update_time'] = df['dUPDATE_TIME'].dt.strftime('%H:%M')  # 提取更新时间的具体时间（小时:分钟）
df['node_time'] = df['dNODE_TIME'].dt.strftime('%H:%M')  # 提取节点时间的具体时间（小时:分钟）

# 统计每个半小时的数据数量
time_range = pd.date_range('2023-11-11 07:00:00', '2023-11-11 19:00:00', freq='30min').time
update_counts = df['update_time'].value_counts().reindex(time_range, fill_value=0)
node_counts = df['node_time'].value_counts().reindex(time_range, fill_value=0)


# 绘制统计图
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
update_counts.plot(kind='bar')
plt.title('Counts for dUPDATE_TIME')
plt.xlabel('Time')
plt.ylabel('Count')

plt.subplot(1, 2, 2)
node_counts.plot(kind='bar')
plt.title('Counts for dNODE_TIME')
plt.xlabel('Time')
plt.ylabel('Count')

plt.tight_layout()
plt.show()
