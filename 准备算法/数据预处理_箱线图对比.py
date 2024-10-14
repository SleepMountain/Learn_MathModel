import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 读取数据
inputfile = r"D:\桌面\竞赛\泰迪杯\2021B题-肥料登记数据分析赛题\附件1.xlsx"
data = pd.read_excel(inputfile, encoding='gbk')


# 定义异常值检测处理函数
def outlier_processing(data, label, method='3σ', threshold=3):
    """
    异常值检测和处理函数
    :param data: DataFrame类型，需要进行异常值检测和处理的数据
    :param label: str类型，需要处理的标签列名
    :param method: str类型，异常值检测和处理的方法，可以选择3σ原则或箱线图，默认为'3σ'
    :param threshold: int或float类型，异常值检测的阈值，当method为'3σ'时表示标准差的倍数，当method为'boxplot'时表示四分位距的倍数，默认为3
    :return: 处理后的DataFrame数据
    """
    # 使用3σ原则进行异常值检测和处理
    if method == '3σ':
        # 计算平均值和标准差
        mean = data[label].mean()
        std = data[label].std()
        # 计算异常值的上下限
        upper_limit = mean + threshold * std
        lower_limit = mean - threshold * std
        # 将超出上下限的数值处理为上下限的值
        data.loc[data[label] > upper_limit, label] = upper_limit
        data.loc[data[label] < lower_limit, label] = lower_limit
    # 使用箱线图进行异常值检测和处理
    elif method == 'boxplot':
        # 计算四分位距和异常值的上下限
        Q1 = data[label].quantile(0.25)
        Q3 = data[label].quantile(0.75)
        IQR = Q3 - Q1
        upper_limit = Q3 + threshold * IQR
        lower_limit = Q1 - threshold * IQR
        # 将超出上下限的数值处理为上下限的值
        data.loc[data[label] > upper_limit, label] = upper_limit
        data.loc[data[label] < lower_limit, label] = lower_limit
    # 如果method参数不正确，则抛出异常
    else:
        raise ValueError('method参数错误，请选择"3σ"或"boxplot"')

    return data


# 对数据进行异常值检测和处理，使用3σ原则和箱线图两种方法
processed_data_3sigma = outlier_processing(data, label='总氮百分比', method='3σ', threshold=3)
processed_data_boxplot = outlier_processing(data, label='总氮百分比', method='boxplot', threshold=3)

# 绘制箱线图，可以直观地展示异常值的分布情况
plt.figure(figsize=(10, 6))
data.boxplot(column='总氮百分比')
plt.title('Original Data Boxplot')
plt.show()

plt.figure(figsize=(10, 6))
processed_data_boxplot.boxplot(column='总氮百分比')
plt.title('Processed Data Boxplot (Boxplot Method)')
plt.show()

# 打印原始数据和处理后的数据
print("原始数据：")
print(data)
print("\n使用3σ原则处理后的数据：")
print(processed_data_3sigma)
print("\n使用箱线图方法处理后的数据：")
print(processed_data_boxplot)
