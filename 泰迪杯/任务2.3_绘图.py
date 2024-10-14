import pandas as pd
import matplotlib.pyplot as plt

# 从 Excel 读取数据
df = pd.read_excel(r"D:\桌面\result8.xlsx")

# 只保留sNODE_NAME占比小于99%的数据
df = df[df['sNODE_NAME'] < 99]

# 将dUPDATE_TIME设为索引
df.set_index('dUPDATE_TIME', inplace=True)

# 绘制堆积面积图
fig, ax = plt.subplots(figsize=(10, 6))
ax.stackplot(df.index, df['iNODE_STATUS'], df['sNODE_NAME'], df['Percentage'], labels=['iNODE_STATUS','sNODE_NAME','Percentage'])
ax.legend(loc='upper left')
ax.set_ylabel('Percentage (%)')
ax.set_title('Stacked Area Plot of Work Processes Over Time')
plt.show()

