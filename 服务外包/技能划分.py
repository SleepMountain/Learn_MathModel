import pandas as pd


# 读取原始数据
input_file_path = r'D:\桌面\竞赛\服务外包\服务外包测试数据.xlsx'
df = pd.read_excel(input_file_path)

# 统计每个月份每种技能出现的次数
skills = df[['投简历月份', '主要技能', '次要技能1', '次要技能2']].melt(id_vars='投简历月份', value_vars=['主要技能', '次要技能1', '次要技能2'], var_name='技能类型', value_name='技能')
monthly_skill_counts = skills.groupby(['投简历月份', '技能']).size().reset_index(name='出现次数')

# 保存每月技能出现次数统计结果到 Excel 文件
output_skills_file_path = r'D:\桌面\竞赛\服务外包\每月技能.xlsx'
monthly_skill_counts.to_excel(output_skills_file_path, index=False)
print("每月技能出现次数统计结果已保存至", output_skills_file_path)
