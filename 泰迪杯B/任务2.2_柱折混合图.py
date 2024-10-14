import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 数据
months = ['3 月', '6 月', '9 月']
revenue = [13415608.48, 37389036.09, 60874611.65]
cost = [8843286.93, 19540240.4, 29276391.8]
profit_margin = [0.811765389, 0.754656261, 0.721555652]
debt_ratio = [0.023865034, 0.027783291, 0.02587737]

# 绘制柱状图
fig, ax1 = plt.subplots()
bar_width = 0.4
index = range(len(months))


ax1.bar(index, revenue, width=bar_width, align='center', alpha=0.7, label='营业总收入', color='skyblue')
ax1.bar([i + bar_width for i in index], cost, width=bar_width, align='center', alpha=0.7, label='营业总成本', color='lightcoral')  # 调整柱条位置
ax1.set_xlabel('月份')
ax1.set_ylabel('金额')
ax1.set_xticks(index)  # 调整 x 轴刻度位置
ax1.set_xticklabels(months)
ax1.legend(loc='upper left')

# 绘制折线图
ax2 = ax1.twinx()
ax2.plot(index, profit_margin, 'g-o', label='利润率')
ax2.plot(index, debt_ratio, 'b-o', label='资产负债率')
ax2.set_ylabel('比率')
ax2.legend(loc='upper right')

plt.title('2019 年企业“T1”经营情况分析')
plt.show()
