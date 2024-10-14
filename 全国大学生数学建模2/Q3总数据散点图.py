import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


file_path = 'D:\桌面\B题\问题三\问题三数据表.xlsx'
sheet_name = '简化表'  # 子表名称
df = pd.read_excel(file_path, sheet_name=sheet_name)

s_f_d = df['半成品决策'].apply(lambda x: str(x).replace('[', '').replace(']', ''))
finished_d = df['非半成品策略']
total_p = df['总利润']

def c_num(decision):
    return int(decision.replace(', ', ''), 2)

numeric = s_f_d.apply(c_num)

filtered_df = df[finished_d.isin([1, 2, 3, 4])]

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(numeric, filtered_df['非半成品策略'], filtered_df['总利润'])

ax.set_xlabel('半成品决策')
ax.set_ylabel('非半成品策略')
ax.set_zlabel('总利润')

cbar = plt.colorbar(scatter)
cbar.set_label('样本点')

plt.title('总利润与决策关系图')
plt.show()