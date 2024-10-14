import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# 读取Excel文件中的指定子表
file_path = r'D:\桌面\B题\问题四\重构前后利润率对比.xlsx'
sheet_name = '问题三'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# 提取两列数据
before_r = data['重构前']
after_r = data['重构后']

# 计算中位数、最大值和最小值
means = [np.mean(before_r), np.mean(after_r)]
medians = [np.median(before_r), np.median(after_r)]
max_values = [np.max(before_r), np.max(after_r)]
min_values = [np.min(before_r), np.min(after_r)]

# 创建葫芦图
fig, ax = plt.subplots(figsize=(8, 6))  # 调整图表大小

violin_parts = ax.violinplot([before_r, after_r], showmeans=True)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 添加标题和标签
ax.set_title('重构前后利润率对比', fontsize=16)
ax.set_ylabel('利润率', fontsize=14)
ax.set_xlabel('重构状态', fontsize=14)
ax.set_xticks([1, 2])
ax.set_xticklabels(['重构前', '重构后'])

# 标注均值、中位数、最大值和最小值
for i, (mean, median, max_val, min_val) in enumerate(zip(means, medians, max_values, min_values), start=1):
    ax.text(i, median, f'中位数: {median:.2f}', horizontalalignment='center', color='red', fontsize=12)
    ax.text(i, max_val, f'最大值: {max_val:.2f}', horizontalalignment='center', color='blue', fontsize=12)
    ax.text(i, min_val, f'最小值: {min_val:.2f}', horizontalalignment='center', color='purple', fontsize=12)

# 调整边距
plt.tight_layout()

# 显示图形
plt.show()