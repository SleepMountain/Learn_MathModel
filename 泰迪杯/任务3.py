import pandas as pd
import json
from pyecharts import options as opts
from pyecharts.charts import Sankey

# 从 Excel 读取数据
file_path = r"D:\桌面\sangjitu.xlsx"
df = pd.read_excel(file_path)

# 构造桑基图所需的节点和链接数据
nodes = []
links = []

# 提取必要的列数据
for i in range(len(df) - 1):
    source_node = str(df.iloc[i, 4])  # Operation 列作为 source 节点
    target_node = str(df.iloc[i + 1, 4])  # Operation 列作为 target 节点
    value = 1  # 设置默认值为1
    links.append({"source": source_node, "target": target_node, "value": value})

nodes = list(set(df["Operation"]))  # nodes 为 Operation 列的唯一值


# 构造 JSON 数据
sankey_data = {"nodes": nodes, "links": links}

# 将数据保存为 JSON 文件
with open("sankey_data.json", "w", encoding="utf-8") as f:
    json.dump(sankey_data, f, ensure_ascii=False)

# 生成桑基图
with open("sankey_data.json", "r", encoding="utf-8-sig") as f:
    j = json.load(f)

c = (
    Sankey()
    .add(
        "sankey",
        nodes=j["nodes"],
        links=j["links"],
        pos_top="10%",
        levels=[
            opts.SankeyLevelsOpts(
                depth=0,
                itemstyle_opts=opts.ItemStyleOpts(color="#fbb4ae"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=1,
                itemstyle_opts=opts.ItemStyleOpts(color="#b3cde3"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=2,
                itemstyle_opts=opts.ItemStyleOpts(color="#ccebc5"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=3,
                itemstyle_opts=opts.ItemStyleOpts(color="#decbe4"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
        ],
        linestyle_opt=opts.LineStyleOpts(curve=0.5),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Sankey-Level Settings"),
        tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),
    )
    .render("sankey_with_level_setting.html")
)
