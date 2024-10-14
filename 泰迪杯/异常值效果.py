import pandas as pd
import seaborn as sns

# 从 Excel 读取数据
file_path = r'D:\桌面\新建 XLSX 工作表 (2).xlsx'
df = pd.read_excel(file_path)

# 忽略小于 0.01 的数据
df = df.applymap(lambda x: x if x >= 0.01 else None)

# 绘制小提琴图
sns.violinplot(data=df[['a', 'b', 'c', 'd']], inner=None)

# 显示图形
import matplotlib.pyplot as plt
plt.show()

