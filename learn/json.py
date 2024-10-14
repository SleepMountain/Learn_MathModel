import asyncio
from aiohttp import TCPConnector, ClientSession

from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import BMapType, ChartType
import pyecharts.options as opts
from pyecharts.charts import Grid, Boxplot, Scatter



y_data = [
    [
        850,
        740,
        900,
        1070,
        930,
        850,
        950,
        980,
        980,
        880,
        1000,
        980,
        930,
        650,
        760,
        810,
        1000,
        1000,
        960,
        960,
    ],
    [
        960,
        940,
        960,
        940,
        880,
        800,
        850,
        880,
        900,
        840,
        830,
        790,
        810,
        880,
        880,
        830,
        800,
        790,
        760,
        800,
    ],
    [
        880,
        880,
        880,
        860,
        720,
        720,
        620,
        860,
        970,
        950,
        880,
        910,
        850,
        870,
        840,
        840,
        850,
        840,
        840,
        840,
    ],
    [
        890,
        810,
        810,
        820,
        800,
        770,
        760,
        740,
        750,
        760,
        910,
        920,
        890,
        860,
        880,
        720,
        840,
        850,
        850,
        780,
    ],
    [
        890,
        840,
        780,
        810,
        760,
        810,
        790,
        810,
        820,
        850,
        870,
        870,
        810,
        740,
        810,
        940,
        950,
        800,
        810,
        870,
    ],
]
scatter_data = [650, 620, 720, 720, 950, 970]

box_plot = Boxplot()

box_plot = (
    box_plot.add_xaxis(xaxis_data=["expr 0", "expr 1", "expr 2", "expr 3", "expr 4"])
    .add_yaxis(series_name="", y_axis=box_plot.prepare_data(y_data))
    .set_global_opts(
        title_opts=opts.TitleOpts(
            pos_left="center", title="Michelson-Morley Experiment"
        ),
        tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(formatter="expr {value}"),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="km/s minus 299,000",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
    )
    .set_series_opts(tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"))
)

scatter = (
    Scatter()
    .add_xaxis(xaxis_data=["expr 0", "expr 1", "expr 2", "expr 3", "expr 4"])
    .add_yaxis(series_name="", y_axis=scatter_data)
    .set_global_opts(
        title_opts=opts.TitleOpts(
            pos_left="10%",
            pos_top="90%",
            title="upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR",
            title_textstyle_opts=opts.TextStyleOpts(
                border_color="#999", border_width=1, font_size=14
            ),
        ),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
        ),
    )
)

grid = (
    Grid()
    .add(
        box_plot,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%", pos_bottom="15%"),
    )
    .add(
        scatter,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%", pos_bottom="15%"),
    )
    .render("boxplot_light_velocity.html")
)

async def get_json_data(url: str) -> dict:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url) as response:
            return await response.json()


# 获取官方的数据
data = asyncio.run(
    get_json_data(
        url="https://echarts.apache.org/examples/data/asset/data/hangzhou-tracks.json"
    )
)

map_data = [[y["coord"] for y in x] for x in data]

(
    BMap(init_opts=opts.InitOpts(width="1200px", height="800px"))
    .add_schema(
        baidu_ak="FAKE_AK",
        center=[120.13066322374, 30.240018034923],
        zoom=14,
        is_roam=True,
        map_style={
            "styleJson": [
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": {"color": "#d1d1d1"},
                },
                {
                    "featureType": "land",
                    "elementType": "all",
                    "stylers": {"color": "#f3f3f3"},
                },
                {
                    "featureType": "railway",
                    "elementType": "all",
                    "stylers": {"visibility": "off"},
                },
                {
                    "featureType": "highway",
                    "elementType": "all",
                    "stylers": {"color": "#fdfdfd"},
                },
                {
                    "featureType": "highway",
                    "elementType": "labels",
                    "stylers": {"visibility": "off"},
                },
                {
                    "featureType": "arterial",
                    "elementType": "geometry",
                    "stylers": {"color": "#fefefe"},
                },
                {
                    "featureType": "arterial",
                    "elementType": "geometry.fill",
                    "stylers": {"color": "#fefefe"},
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": {"visibility": "off"},
                },
                {
                    "featureType": "green",
                    "elementType": "all",
                    "stylers": {"visibility": "off"},
                },
                {
                    "featureType": "subway",
                    "elementType": "all",
                    "stylers": {"visibility": "off"},
                },
                {
                    "featureType": "manmade",
                    "elementType": "all",
                    "stylers": {"color": "#d1d1d1"},
                },
                {
                    "featureType": "local",
                    "elementType": "all",
                    "stylers": {"color": "#d1d1d1"},
                },
                {
                    "featureType": "arterial",
                    "elementType": "labels",
                    "stylers": {"visibility": "off"},
                },
                {
                    "featureType": "boundary",
                    "elementType": "all",
                    "stylers": {"color": "#fefefe"},
                },
                {
                    "featureType": "building",
                    "elementType": "all",
                    "stylers": {"color": "#d1d1d1"},
                },
                {
                    "featureType": "label",
                    "elementType": "labels.text.fill",
                    "stylers": {"color": "#999999"},
                },
            ]
        },
    )
    .add(
        series_name="",
        type_=ChartType.LINES,
        data_pair=map_data,
        is_polyline=True,
        is_large=True,
        linestyle_opts=opts.LineStyleOpts(color="purple", opacity=0.6, width=1),
        effect_opts=opts.EffectOpts(trail_length=0.5),
    )
    .add_control_panel(
        copyright_control_opts=opts.BMapCopyrightTypeOpts(position=3),
        maptype_control_opts=opts.BMapTypeControlOpts(
            type_=BMapType.MAPTYPE_CONTROL_DROPDOWN
        ),
        scale_control_opts=opts.BMapScaleControlOpts(),
        overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),
        navigation_control_opts=opts.BMapNavigationControlOpts(),
        geo_location_control_opts=opts.BMapGeoLocationControlOpts(),
    )
    .render("hiking_trail_in_hangzhou.html")
)
