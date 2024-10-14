import pandas as pd

# 读取原始Excel表格数据
df = pd.read_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result6.xlsx")

# 创建新的Excel表格
new_df = pd.DataFrame(columns=['操作人员ID', '工序', '工作时长', '完成案卷的数量'])


# 遍历原始数据，计算工作时长和完成案卷的数量
for index, row in df.iterrows():
    arch_id = row['sARCH_ID']
    node_name = row['sNODE_NAME']
    user_id = row['iUSER_ID']
    start_time = row['dUPDATE_TIME']
    end_time = row['dNODE_TIME']

    # 计算一次处理时间
    time_diff = end_time - start_time

    # 检查该操作人员ID和工序是否已存在于新表格中
    existing_row = new_df.loc[(new_df['操作人员ID'] == user_id) & (new_df['工序'] == node_name)]
    if existing_row.empty:
        # 如果不存在，添加新行
        new_row = {'操作人员ID': user_id, '工序': node_name, '工作时长': time_diff, '完成案卷的数量': 1}
        new_df = new_df.append(new_row, ignore_index=True)
    else:
        # 如果已存在，更新工作时长和完成案卷的数量
        existing_row_index = existing_row.index[0]
        new_df.at[existing_row_index, '工作时长'] += time_diff
        new_df.at[existing_row_index, '完成案卷的数量'] += 1

# 将新表格保存为Excel文件
new_df.to_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result7.xlsx", index=False)