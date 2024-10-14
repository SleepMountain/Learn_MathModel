import pandas as pd

# 读取Excel表格数据
df = pd.read_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/data.xlsx")

# 筛选出所有带有“自检全检”工序返工的记录
filtered_df = df[(df['sNODE_NAME'] == '自检全检') & (df['iNODE_STATUS'] == 5)]

# 统计每个操作人员的总工序数量
total_processes = df.groupby('iUSER_ID').size()


# 统计每个操作人员被返工的工序数量
rework_processes = filtered_df.groupby('iUSER_ID').size()

# 计算百分比
percentages = (rework_processes / total_processes)

    # 创建新的Excel表格并写入百分比数据
result_df = pd.DataFrame({'操作人员ID': percentages.index, '被返工的工序占比': percentages.values})
result_df.to_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result8.xlsx", index=False)