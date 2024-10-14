import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

# 创建图的邻接矩阵
adj_matrix = np.array([
    [0, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 0]
])


# 创建图
G = nx.DiGraph(adj_matrix)

# 定义需求量
demands = [
    (1, 5, 100),
    (1, 6, 150),
    (1, 8, 200),
    (1, 9, 180),
    (2, 4, 160),
    (2, 6, 110),
    (2, 7, 120),
    (2, 9, 140),
    (3, 4, 130),
    (3, 5, 150),
    (3, 7, 140),
    (3, 8, 160),
    (4, 2, 100),
    (4, 3, 170),
    (4, 8, 190),
    (4, 9, 120),
    (5, 1, 160),
    (5, 3, 140),
    (5, 7, 180),
    (5, 9, 100),
    (6, 1, 170),
    (6, 2, 120),
    (6, 7, 130),
    (6, 8, 200),
    (7, 2, 120),
    (7, 3, 150),
    (7, 5, 190),
    (7, 6, 100),
    (8, 1, 130),
    (8, 3, 180),
    (8, 4, 140),
    (8, 6, 150),
    (9, 1, 170),
    (9, 2, 130),
    (9, 4, 190),
    (9, 5, 160),
]


# 计算所有路径
def get_all_paths(graph, start, end, max_depth=5):
    paths = []

    def _find_paths(path):
        node = path[-1]
        if len(path) > max_depth:
            return
        if node == end:
            paths.append(path)
            return
        for neighbor in graph.neighbors(node):
            if neighbor not in path:
                _find_paths(path + [neighbor])

    _find_paths([start])
    return paths


# 生成并打印所有路径
all_paths = {}
for start, end, _ in demands:
    start, end = start - 1, end - 1  # 调整为0基索引
    paths = get_all_paths(G, start, end)
    all_paths[(start + 1, end + 1)] = paths  # 恢复为1基索引
    print(f"Paths from {start + 1} to {end + 1}:")

    for i, path in enumerate(paths):
        # 创建一个子图用于绘图
        fig, ax = plt.subplots(figsize=(8, 6))

        # 复制原始图以便突出显示路径
        H = G.copy()

        # 设置路径上的边颜色
        path_edges = [(path[j], path[j + 1]) for j in range(len(path) - 1)]
        edge_colors = ['red' if (u, v) in path_edges or (v, u) in path_edges else 'gray' for u, v in H.edges()]

        # 设置节点颜色
        node_colors = ['green' if n in path else 'lightblue' for n in H.nodes()]

        # 使用 spring 布局
        pos = nx.spring_layout(H)

        # 绘制图
        nx.draw(H, pos, with_labels=True, labels={i: str(len(adj_matrix) - i) for i in range(len(adj_matrix))},
                node_color=node_colors, node_size=500, edge_color=edge_colors,
                font_size=10, font_weight='bold', ax=ax)

        # 添加标题
        plt.title(f"Path {i + 1} from {start + 1} to {end + 1}")

        # 保存图片
        plt.savefig(f"path_{start + 1}_to_{end + 1}_{i + 1}.png")
        plt.close(fig)  # 关闭绘图窗口

        # 恢复为1基索引
        print(" -> ".join(map(str, [p + 1 for p in path])))
    print()