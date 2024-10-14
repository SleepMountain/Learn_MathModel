"""读取数据的方法"""
def read_input(file_path):
    with open(file_path, 'r') as file:
        n, m = map(int, file.readline().split())                         # 采样点数量和候选机位数量
        cover = {i: [] for i in range(0, m)}                             # 初始化候选机位到采样点的映射
        e_count = [0] * (n + 1)                                          # 初始化采样点的覆盖计数


        for _ in range(n):
            e_id = int(file.readline().strip())                          # 读取元素ID
            cover_count = int(file.readline().strip())                   # 读取该元素被覆盖次数
            cover_ids = list(map(int, file.readline().strip().split()))  # 读取覆盖该元素的集合编号
            e_count[e_id] = cover_count                                  # 更新元素覆盖计数
            for id in cover_ids:
                cover[id].append(e_id)                                   # 记录覆盖关系

    return n, m, cover, e_count

"""遗传算法"""
def greedy_cover(cover, e_counts, n, m):
    e_covered = set()                                                    # 初始化集合，存储已覆盖的采样点
    selected = []                                                        # 初始化集合，存储已选择的集合编号

    while len(e_covered) < n:                                            # 不满足全覆盖条件
        new = 0                                                          # 初始化，存储覆盖数
        best = None                                                      # 初始化，存储最佳覆盖集合id

        for set_id, covered_ine in cover.items():                        # 遍历字典
            uncovered = set(covered_ine) - e_covered                     # 计算未被覆盖的元素集合
            if len(uncovered) > new and set_id not in selected:          # 新覆盖采样点数大于当前且该集合未被选中
                new = len(uncovered)                                     # 替换
                best = set_id

        if best is None:                                                 # 理论不会出现
            print("无法进一步覆盖剩余采样点")
            break

        selected.append(best)                                            # 将找到的最佳集合编号添加到已选集合列表
        e_covered.update(cover[best])                                    # 将最佳集合覆盖的所有采样点加入已覆盖集合

    return selected, e_covered

"""检查方法，解题可以不用"""
def check(solution, cover, n):
    new = []                                                              # 收集所有被选集合覆盖的采样点
    dict = {}                                                             # 记录每个采样点被覆盖的次数
    missing = []                                                          # 存放未被任何选中集合覆盖的采样点编号
    for i in solution:
        value = cover[i]
        new.extend(value)
        for num in value:
            dict[num] = dict.get(num, 0) + 1                              # 覆盖计数

    for num in range(0, n):                                               # 统计没出现的
        if num not in dict:
            missing.append(num)

    repeated_ids = [num for num, count in dict.items() if count > 1]      # 重复的输出

    return repeated_ids, missing

"""主函数"""
def main():
    input_file = r'D:\桌面\大二\数据结构2\SetCoveringTestData\Test05.txt'
    n, m, cover, _ = read_input(input_file)
    solution, _ = greedy_cover(cover, [0] * n, n, m)                      # 用全0初始化元素覆盖计数（不用也可以，防止数据有空）

    print(len(solution))                                                  # 输出选中的候选机位数量
    print(*solution)                                                      # 输出选中的候选机位
    # print("\n选中的集合包含的采样点：")
    # for set_id in solution:
    #     print(f"集合{set_id}: {cover[set_id]}")
    #
    repeated_ids, missing = check(solution, cover, n)
    print("\n验证结果：")
    print(f"重复覆盖的采样点数量: {len(repeated_ids)}")
    # print(f"重复覆盖的采样点数量: {len(repeated_ids)}, 重复的采样点: {repeated_ids}")
    print(f"未覆盖的采样点数量: {len(missing)}, 未覆盖的采样点: {missing}")

"""启动函数"""
if __name__ == "__main__":
    main()
