import pandas as pd
import numpy as np
from scipy.stats import genextreme


# 读取数据
data = pd.read_excel('D:/桌面/竞赛/数模/暑假训练/progress2/问题一极端天气表.xlsx')

# 提取降水信息
precipitation_data = data.iloc[:, 3:]  # 提取第4列及以后的数据，即降水信息

# 根据极值分布模型将大于50的数据设为极端事件
extreme_data = precipitation_data.applymap(lambda x: x if x <= 50 else np.nan)

# 极值分布模型拟合
fitted_parameters = []
for column in extreme_data:
    # 去除缺失值并拟合极值分布模型
    series = extreme_data[column].dropna()
    params = genextreme.fit(series)
    fitted_parameters.append(params)

# 计算观测数据与模拟数据之间的差异
observed_parameters = []
for column in precipitation_data:
    series = precipitation_data[column]
    params = genextreme.fit(series.dropna())
    observed_parameters.append(params)

# 创建一个新的数据框来存储结果
result_df = pd.DataFrame()

# 打印模拟数据与观测数据的参数差异
for i in range(len(fitted_parameters)):
    obs_params = observed_parameters[i]
    fit_params = fitted_parameters[i]
    result_df["地区{}".format(i + 1)] = ["观测数据"] + list(obs_params) + ["模拟数据"] + list(fit_params)

# 预测未来可能的极端事件情况
future_data = []  # 存储预测结果
for params in fitted_parameters:
    loc, scale, shape = params
    threshold = 50  # 阈值，设定为50
    exceedance_prob = genextreme.sf(threshold, shape, loc, scale)
    future_data.append(exceedance_prob)

# 对未来可能的极端事件进行分位点投影变换，并存储结果到数据框中
for i in range(len(fitted_parameters)):
    obs_params = observed_parameters[i]
    fit_params = fitted_parameters[i]
    obs_loc, obs_scale, obs_shape = obs_params
    fit_loc, fit_scale, fit_shape = fit_params

    # 计算观测数据和模拟数据的分布差异
    delta_loc = obs_loc - fit_loc
    delta_scale = obs_scale / fit_scale
    delta_shape = obs_shape - fit_shape

    # 对未来可能的极端事件进行分位点投影变换
    future_exceedance_prob = future_data[i]
    corrected_exceedance_prob = genextreme.ppf(future_exceedance_prob, delta_shape, delta_loc, delta_scale)

    result_df["地区{}".format(i + 1)].iloc[-1] = corrected_exceedance_prob

# 将结果保存为Excel文件
result_df.to_excel('D:\桌面\竞赛\数模\暑假训练\progress2\极值分布输出结果.xlsx', index=False)
