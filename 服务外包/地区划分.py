import pandas as pd

# 读取原始数据
input_file_path = r'D:\桌面\竞赛\服务外包\服务外包测试数据.xlsx'
df = pd.read_excel(input_file_path)


# 统计每个地区的数据量
province_counts = df['地区'].value_counts().reset_index()
province_counts.columns = ['地区', '数据量']

# 保存每地区数据量统计结果到 Excel 文件
output_province_file_path = r'D:\桌面\竞赛\服务外包\每地区数据.xlsx'
province_counts.to_excel(output_province_file_path, index=False)
print("地区数据量统计结果已保存至", output_province_file_path)
