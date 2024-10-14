import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import linprog

# 调整邻接矩阵以匹配1到9的节点编号
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


# 创建图，并添加1到9的节点
G = nx.DiGraph()
G.add_nodes_from(range(1, 10))  # 添加1到9的节点
G.add_edges_from([(i+1, j+1) for i, row in enumerate(adj_matrix) for j, x in enumerate(row) if x == 1])

# 绘制图形
pos = nx.spring_layout(G)  # 使用 spring 布局
labels = {i: str(i) for i in G.nodes()}
nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=500, edge_color='gray', font_size=10, font_weight='bold')
plt.title("Directed Graph from Adjacency Matrix")
plt.show()


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


# 定义每条边的突发状况概率
p_failure = 0.1  # 每条边发生故障的概率


# 计算路径可达率
def calculate_reliability(path, adj_matrix):
    reliability = 1.0
    for i in range(len(path) - 1):
        if adj_matrix[path[i] - 1, path[i + 1] - 1] > 0:
            reliability *= (1 - p_failure)
    return reliability


# 生成所有路径
all_paths = {}
for start, end, demand in demands:
    all_paths[(start, end)] = get_all_paths(G, start, end)


# 优化流量分配
def optimize_flows(paths, demand):
    num_paths = len(paths)
    c = [-1] * num_paths  # 目标函数，最大化总流量
    A_eq = np.zeros((1, num_paths))
    b_eq = np.array([demand])

    # 构建约束矩阵
    for i, path in enumerate(paths):
        reliability = calculate_reliability(path, adj_matrix)
        A_eq[0, i] += reliability

    bounds = [(0, None)] * num_paths
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    if result.success:
        return -result.fun, result.x
    else:
        return 0, []


# 输出结果
def output_results():
    results = []
    for (start, end), paths in all_paths.items():
        demand = [d for s, e, d in demands if s == start and e == end][0]
        max_flow, path_flows = optimize_flows(paths, demand)

        # 收集结果
        for i, path in enumerate(paths):
            path_str = '-'.join(map(str, path))
            flow = path_flows[i] if i < len(path_flows) else 0
            results.append((start, end, path_str, flow))

    return results


results = output_results()

# 打印结果
print("起点,终点\t规划路径\t\t\t\t\t\t分配交通量")
for start, end, path_str, flow in results:
    print(f"({start},{end})\t{path_str}\t\t{flow:.2f}")
