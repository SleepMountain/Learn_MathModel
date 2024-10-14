from pyecharts.charts import Bar3D
import pyecharts.options as opts

data = [
    [416, 0, 0.721555652],
    [46, 1, 0.555489895],
    [300059, 2, 0.535591843]
]

x_data = [d[0] for d in data]
y_data = [d[1] for d in data]
z_data = [d[2] for d in data]

color_map = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8']


bar3d = (
    Bar3D()
    .add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(data=x_data),
        yaxis3d_opts=opts.Axis3DOpts(data=y_data),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=max(z_data), pieces=[
            {"min": z_min, "max": z_max, "color": color} for z_min, z_max, color in zip([0]+z_data[:-1], z_data, color_map)
        ]),
        title_opts=opts.TitleOpts(title="2019年该行业各细类利润率对比"),
    )
)

bar3d.render("bar_chart.html")
