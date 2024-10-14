import pandas as pd

# 读取原始Excel表格数据
data = pd.read_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result6.xlsx")

# 筛选需要的字段
fields = ['sARCH_ID', 'sNODE_NAME', 'iNODE_STATUS', 'iUSER_ID', 'dUPDATE_TIME', 'dNODE_TIME']
df = data[fields]

# 新建数据框用来存放新的结果
new_df = pd.DataFrame(columns=['操作人员ID', '工序', '工作时长', '完成案卷的数量'])

# 遍历每位操作人员ID
for user_id in df['iUSER_ID'].unique():
    # 按操作人员ID筛选数据
    user_data = df[df['iUSER_ID'] == user_id]


    # 初始化工作时长和完成案卷的数量为0
    work_duration = 0
    num_completed_cases = 0

    # 遍历每个工序
    for node_name in user_data['sNODE_NAME'].unique():
        # 按工序筛选数据
        node_data = user_data[user_data['sNODE_NAME'] == node_name]

        # 计算工作时长
        durations = (node_data['dNODE_TIME'] - node_data['dUPDATE_TIME']).dt.total_seconds() / 3600
        work_duration += durations.sum()

        # 计算完成案卷的数量
        num_completed_cases += node_data.shape[0]

        # 将计算结果添加到新的数据框中
        new_row = {'操作人员ID': user_id, '工序': node_name, '工作时长': work_duration, '完成案卷的数量': num_completed_cases}
        new_df = new_df.append(new_row, ignore_index=True)

# 将结果保存到新的Excel表格中
new_df.to_excel("D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result8.xlsx", index=False)