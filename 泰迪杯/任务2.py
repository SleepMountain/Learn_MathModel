import pandas as pd

# 读取excel数据
df = pd.read_excel(r'D:\桌面\result2.xlsx')

# 将时间列转换为datetime格式，并抽取日期部分
df['dNODE_TIME'] = pd.to_datetime(df['dNODE_TIME']).dt.date

# 计算每天不同工序完成案卷数量
grouped = df.groupby(['dNODE_TIME', 'iFLOW_NODE_NO']).size().reset_index(name='counts')

# 提取数据
dates = grouped['dNODE_TIME'].unique()
flows = grouped['iFLOW_NODE_NO'].unique()
data = []
for d in dates:
    subset = grouped[grouped['dNODE_TIME'] == d]
    for f in flows:
        count = subset[subset['iFLOW_NODE_NO'] == f]['counts'].values
        if len(count) > 0:
            data.append([str(d), str(f), int(count[0])])


# 创建包含你的数据的新 DataFrame
result_df = pd.DataFrame(data, columns=['Date', 'Flow', 'Count'])

# 将结果保存到 Excel 文件
result_file_path = r'D:\桌面\result4.xlsx'
result_df.to_excel(result_file_path, index=False)
