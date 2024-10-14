import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product

file_path = 'D:\桌面\B题\问题三\问题三数据表.xlsx'
sheet_name = '11101111'
data = pd.read_excel(file_path, sheet_name=sheet_name)


half_p_d = ['[1, 1, 1]', '[1, 1, 0]', '[1, 0, 1]', '[1, 0, 0]', '[0, 1, 1]', '[0, 1, 0]', '[0, 0, 1]', '[0, 0, 0]']
p_d = ['0a', '0b', '1a', '1b']

all_combinations = list(product(half_p_d, p_d))

df = pd.DataFrame(all_combinations, columns=['半成品决策', '成品决策'])
df['总销售金额'] = 0.0

df = df.merge(data[['半成品决策', '成品决策', '总销售金额']], on=['半成品决策', '成品决策'], how='left')
df['总销售金额'] = df['总销售金额_y'].fillna(df['总销售金额_x'])
df.drop(['总销售金额_x', '总销售金额_y'], axis=1, inplace=True)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

norm = plt.Normalize(df['总销售金额'].min(), df['总销售金额'].max())
colors = plt.cm.viridis(norm(df['总销售金额']))

for i, (half, prod, profit) in enumerate(zip(df['半成品决策'], df['成品决策'], df['总销售金额'])):
    if not np.isnan(profit):
        x = half_p_d.index(half)
        y = p_d.index(prod)
        z = profit
        ax.bar3d(x, y, 0, 0.6, 0.6, z, color=colors[i], shade=True)

ax.set_xticks(range(len(half_p_d)))
ax.set_xticklabels(half_p_d, rotation=45, ha='right', fontsize=10)
ax.set_yticks(range(len(p_d)))
ax.set_yticklabels(p_d, fontsize=10)
ax.set_zlabel('总销售金额', fontsize=12)

ax.set_title('总销售金额随成品决策和半成品决策的变化', fontsize=15)

mappable = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
mappable.set_array(df['总销售金额'])
cbar = plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('总销售金额', fontsize=12)

ax.grid(True)

plt.show()