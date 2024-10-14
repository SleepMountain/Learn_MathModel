import pandas as pd


# 加载数据表
data = pd.read_excel('D:\桌面\竞赛\数模\暑假训练\progress2\问题一极端天气表.xlsx')

# 提取前三列年月日信息
date_info = data.iloc[:, 0:3]

# 提取降水信息列
precipitation_data = data.iloc[:, 3:]

# 存储极端降水出现的时间和地区的代码
extreme_precipitation_info = []

# 遍历每个地区的降水数据
for idx, row in precipitation_data.iterrows():
    extreme_precipitation_idxs = (row > 50).to_numpy().nonzero()[0]
    if len(extreme_precipitation_idxs) > 0:
        area_codes = precipitation_data.columns[extreme_precipitation_idxs]
        times = '-'.join(str(x) for x in date_info.loc[idx].values)
        for area_code in area_codes:
            extreme_precipitation_info.append([area_code, times])

print("每次极端降水出现的时间和地区的代码：")
for info in extreme_precipitation_info:
    print(info)
