import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


file_path = r'D:\桌面\问题四针对问题三1.xlsx'
sheet_name = 'Sheet3'
df = pd.read_excel(file_path, sheet_name=sheet_name)

fig, ax1 = plt.subplots(figsize=(12, 8), dpi=100)

bars = ax1.bar(df['Best Decision ID'], df['计数'], color='b', alpha=0.5, label='计数')
ax1.set_xlabel('Best Decision', fontsize=14)
ax1.set_ylabel('计数', color='b', fontsize=14)
ax1.tick_params('y', colors='b')

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom', fontsize=12)

ax2 = ax1.twinx()
line, = ax2.plot(df['Best Decision ID'], df['占比']*100, color='r', marker='o', label='占比')
ax2.set_ylabel('占比', color='r', fontsize=14)
ax2.tick_params('y', colors='r')

plt.title('各策略的计数和占比', fontsize=16)

fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))

plt.xticks(rotation=90, ha='right')

plt.grid(True)
plt.show()