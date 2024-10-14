import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

file_path = r'D:\桌面\B题\问题四\重构前后利润率对比.xlsx'
sheet_name = '问题二'
df = pd.read_excel(file_path, sheet_name=sheet_name)

situations = df['情况'].values[:6]
strategies = df['策略'].apply(lambda x: str(x)[1:-1].replace(', ', ',')).unique()[:16]
profit_increase_percentage = df['利润提高百分比'].values.reshape(6, 16)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

X = np.arange(len(strategies))
Y = np.arange(len(situations))
X, Y = np.meshgrid(X, Y)
Z = profit_increase_percentage

colors = cm.inferno(Z / np.max(Z))  # 使用inferno配色方案
for i in range(len(situations)):
    for j in range(len(strategies)):
        ax.bar3d(j, i, 0, 0.8, 0.8, Z[i, j], color=colors[i, j], shade=True)

ax.set_xlabel('策略', labelpad=10)
ax.set_ylabel('情况', labelpad=10)
ax.set_zlabel('利润提高百分比', labelpad=10)

ax.set_xticks(np.arange(len(strategies)))
ax.set_yticks(np.arange(len(situations)))
ax.set_xticklabels([f'{k+1}' for k in range(len(strategies))], rotation=45, ha='right')
ax.set_yticklabels(situations)

ax.set_title('重构前后利润率对比', pad=20)

ax.view_init(elev=30, azim=45)  # 更全面的角度

plt.show()