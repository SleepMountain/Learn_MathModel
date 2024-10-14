import pandas as pd
import numpy as np
def pearson_correlation(x, y):
    # 计算平均值
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    # 计算标准差
    std_dev_x = np.std(x)
    std_dev_y = np.std(y)


    # 计算标准化后的变量
    x_normalized = (x - mean_x) / std_dev_x
    y_normalized = (y - mean_y) / std_dev_y

    # 计算皮尔逊相关系数
    cov = np.cov(x_normalized, y_normalized, bias=True)[0][1]
    corrcoef = cov / (std_dev_x * std_dev_y)

    return corrcoef

# 读取数据
df = pd.read_csv('RL_new1.csv')

# 获取所有列名
columns = df.columns.tolist()

# 计算每两个指标之间的皮尔逊相关系数并存储在字典中
correlation_dict = {}
for i in range(len(columns)):
    for j in range(i+1, len(columns)):
        x = df[columns[i]]
        y = df[columns[j]]
        corr_coef = pearson_correlation(x, y)
        correlation_dict[(columns[i], columns[j])] = corr_coef

# 打印皮尔逊相关系数
for key, value in correlation_dict.items():
    print(f"Correlation between {key[0]} and {key[1]}: {value}")