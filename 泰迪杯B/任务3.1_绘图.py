import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pyecharts.charts import HeatMap
import pyecharts.options as opts


# 读取数据
df = pd.read_csv("D:\桌面\\financial_data.csv")

# 计算所有属性之间的相关性
correlation_matrix = df.corr()

# 创建热力图数据
data = []
for col in correlation_matrix.columns:
    correlation_values = []
    for col2 in correlation_matrix.columns:
        correlation_values.append(correlation_matrix[col][col2])
    data.append(correlation_values)

# 绘制热力图
xaxis_data = list(correlation_matrix.columns)
yaxis_data = list(correlation_matrix.columns)
(
    HeatMap()
    .add_xaxis(xaxis_data)
    .add_yaxis(
        series_name="Correlation",
        yaxis_data=yaxis_data,
        value=data,
        label_opts=opts.LabelOpts(is_show=True, color="#fff", position="bottom", horizontal_align="50%"),
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(type_="category", axislabel_opts=opts.LabelOpts(interval=0)),  # 设置刻度间隔为0
        yaxis_opts=opts.AxisOpts(type_="category", axislabel_opts=opts.LabelOpts(rotate=-45, interval=0)),  # 设置刻度间隔为0
        visualmap_opts=opts.VisualMapOpts(min_=-1, max_=1, is_calculable=True, orient="horizontal", pos_left="center"),
    )
    .render("heatmap.html")
)
