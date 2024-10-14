import pandas as pd


# 加载数据表
data = pd.read_excel('D:\桌面\竞赛\数模\暑假训练\progress2\问题一极端天气表.xlsx')

# 提取前三列年月日信息
date_info = data.iloc[:, 0:3]

# 提取降水信息列
precipitation_data = data.iloc[:, 3:]

# 存储极端降水出现的时间和地区的字典
extreme_precipitation_info = {}

# 遍历每个地区的降水数据
for area_code in precipitation_data.columns:
    area_dates = []
    for idx, row in date_info.iterrows():
        date = '-'.join(str(x) for x in row.values)
        if precipitation_data.loc[idx, area_code] > 50:
            area_dates.append(date)
    if len(area_dates) > 0:
        extreme_precipitation_info[area_code] = area_dates

print("每个地区的极端降水日期和时间：")
for area_code, dates in extreme_precipitation_info.items():
    print(area_code, dates)
