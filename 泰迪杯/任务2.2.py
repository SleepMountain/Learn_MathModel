import pandas as pd
from pyecharts.charts import Line
import pyecharts.options as opts

# 读取数据
df = pd.read_excel("D:\\桌面\\data.xlsx", engine='openpyxl')

# 将时间列转换为datetime类型
df['dUPDATE_TIME'] = pd.to_datetime(df['dUPDATE_TIME'])
df['dNODE_TIME'] = pd.to_datetime(df['dNODE_TIME'])

# 定义一个函数来计算和调整工作量
def calculate_workload(row):
    workload = (row['dNODE_TIME'] - row['dUPDATE_TIME']).total_seconds() / 3600
    if workload > 24:
        days = int(workload // 24)
        remainder = workload % 24
        workload = days * 8.5 + min(8.5, remainder)
    return workload


# 应用函数并计算工作量
df['workload'] = df.apply(calculate_workload, axis=1)

# 按照日期和工序种类分组，对工作量进行求和
df_daily = df.groupby([df['dUPDATE_TIME'].dt.date, 'iFLOW_NODE_NO'])['workload'].sum().reset_index()

# 转换 'dUPDATE_TIME' 列为 datetime 类型
df_daily['dUPDATE_TIME'] = pd.to_datetime(df_daily['dUPDATE_TIME'])

# 将 'dUPDATE_TIME' 列转换为字符串格式
df_daily['dUPDATE_TIME'] = df_daily['dUPDATE_TIME'].dt.strftime('%Y-%m-%d')

# 模拟数据，你需要根据自己的数据进行相应的修改
x_data = df_daily['dUPDATE_TIME'].unique().tolist()  # 使用日期作为 x 轴数据
y_data = df_daily.pivot(index='dUPDATE_TIME', columns='iFLOW_NODE_NO', values='workload').fillna(0).values.T.tolist()  # 使用工序种类作为堆叠区域图的 y 轴数据

line = (
    Line()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="工序 1",
        y_axis=y_data[0],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="工序 2",
        y_axis=y_data[1],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="工序 3",
        y_axis=y_data[2],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="工序 4",
        y_axis=y_data[3],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(title="制各工序每天投入工作量"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
)

# 保存为 HTML 文件
line.render("daily_workload.html")
