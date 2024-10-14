import pandas as pd


# 读取Excel文件
file_path = r'D:\桌面\竞赛\服务外包\服务外包测试数据.xlsx'
df = pd.read_excel(file_path)

# 统计每个月每个职业的数据量
monthly_occupation_counts = df.groupby(['投简历月份', '职业']).size().reset_index(name='数据量')

# 保存统计结果到Excel文件
output_file_path = r'D:\桌面\竞赛\服务外包\月度职业数据量统计.xlsx'
monthly_occupation_counts.to_excel(output_file_path, index=False)

print("数据已保存到Excel文件:", output_file_path)
