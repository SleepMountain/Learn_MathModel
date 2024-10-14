import pandas as pd

# 加载数据表
data = pd.read_excel('D:\桌面\竞赛\数模\暑假训练\progress2\问题一极端天气表.xlsx')


# 提取前三列年月日信息
date_info = data.iloc[:, 0:3]


# 提取降水信息列
precipitation_data = data.iloc[:, 3:]

# 存储每年的极端降水地区和数量
yearly_extreme_precipitation = {}

# 遍历每行数据
for idx, row in precipitation_data.iterrows():
    year = date_info.loc[idx, '年']
    extreme_precipitation_idxs = (row > 50).to_numpy().nonzero()[0]
    if len(extreme_precipitation_idxs) > 0:
        area_codes = precipitation_data.columns[extreme_precipitation_idxs]
        if year not in yearly_extreme_precipitation:
            yearly_extreme_precipitation[year] = []
        yearly_extreme_precipitation[year].extend(area_codes)

# 统计每年极端降水的数量
yearly_count = {year: len(set(area_codes)) for year, area_codes in yearly_extreme_precipitation.items()}

print("每年的极端降水数据数量：")
for year, count in yearly_count.items():
    print(f"年份：{year}，数据数量：{count}")
