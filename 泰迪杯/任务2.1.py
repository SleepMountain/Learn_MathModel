import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar3D

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


# 绘制3D柱状图
c = (
    Bar3D()
    .add(
        "",
        [[d, f, int(count)] for d, f, count in data],
        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=list(map(str, dates))),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=list(map(str, flows))),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            is_calculable=True,
            dimension=1,
            max_=grouped['counts'].max(),
            range_color=["#313695", "#4575b4", "#75add1", "#abd9e9", "#e0f3f8"]
        ),
        title_opts=opts.TitleOpts(title="每天不同工序完成案卷数量"),
    )
    .render("bar3d.html")
)


