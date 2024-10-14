import pandas as pd
from pyecharts.charts import HeatMap
import pyecharts.options as opts

# 读取数据
df = pd.read_csv("D:\桌面\\financial_data.csv")

# 计算相关性
correlation = df.corr()['LRZE'].sort_values(ascending=False)

# 挑选相关度最高的 5 个指标
top_5_correlated = correlation[1:6]

# 输出相关度最高的 5 个指标
print(top_5_correlated)


# 创建热力图数据
data = []
for col in top_5_correlated.index:
    correlation_values = []
    for col2 in top_5_correlated.index:
        correlation_values.append(df[col].corr(df[col2]))
    data.append(correlation_values)

# 绘制热力图
xaxis_data = list(top_5_correlated.index)
yaxis_data = list(top_5_correlated.index)
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
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(type_="category"),
        visualmap_opts=opts.VisualMapOpts(min_=-1, max_=1, is_calculable=True, orient="horizontal", pos_left="center"),
    )
    .render("correlation_heatmap.html")
)
