import pandas as pd


# 读取原始数据
input_file_path = r'D:\桌面\竞赛\服务外包\服务外包测试数据.xlsx'
df = pd.read_excel(input_file_path)

# 合并主要技能、次要技能1 和 次要技能2 列，并统计每种职业的数据量
skills_df = df[['主要技能', '次要技能1', '次要技能2']].melt(value_name='职业').dropna()
job_counts = skills_df['职业'].value_counts().reset_index()
job_counts.columns = ['职业', '数据量']

# 保存每种职业数据量统计结果到 Excel 文件
output_job_file_path = r'D:\桌面\竞赛\服务外包\每种职业数据量.xlsx'
job_counts.to_excel(output_job_file_path, index=False)
print("每种职业数据量统计结果已保存至", output_job_file_path)
