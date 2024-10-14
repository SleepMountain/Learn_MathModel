from pyecharts.charts import Line
import pyecharts.options as opts

x_data = [
    "2018Q1", "2018Q2", "2018Q3", "2018Q4",
    "2019Q1", "2019Q2", "2019Q3"
]
y_data = {
    "公用事业": [0.123878, 0.134898, 0.130161, 0.039014, 0.071129, 0.109629, 0.113035],
    "商业": [0.059997, 0.036759, 0.026649, 0.020995, 0.038165, 0.043507, 0.046038],
    "工业": [0.098394, 0.098617, 0.097515, 0.061311, 0.075916, 0.089433, 0.090214],
    "房地产": [0.138546, 0.128353, 0.118209, 0.118550, 0.110268, 0.132033, 0.115361],
    "综合": [0.042386, 0.017834, 0.047833, -0.045770, -0.025029, 0.036441, 0.029525],
    "金融": [0.212397, 0.219324, 0.281944, 0.186477, 0.358575, 0.256588, 0.221770]
}


line = Line()

for industry, profits in y_data.items():
    line.add_xaxis(x_data)
    line.add_yaxis(
        series_name=industry,
        y_axis=profits,
        is_smooth=True,
        label_opts=opts.LabelOpts(is_show=False)
    )

line.set_global_opts(
    title_opts=opts.TitleOpts(title="各行业利润额季度变化"),
    tooltip_opts=opts.TooltipOpts(trigger="axis"),
    xaxis_opts=opts.AxisOpts(type_="category"),
    yaxis_opts=opts.AxisOpts(type_="value")
)

line.render("line_chart.html")
