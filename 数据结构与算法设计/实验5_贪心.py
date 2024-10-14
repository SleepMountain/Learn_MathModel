"""读取数据的方法"""
def read_input(file_path):
    with open(file_path, 'r') as file:
        n, m = map(int, file.readline().split())
        cover = {i: [] for i in range(0, m)}
        e_count = [0] * (n + 1)


        for _ in range(n):
            e_id = int(file.readline().strip())
            cover_count = int(file.readline().strip())
            cover_ids = list(map(int, file.readline().strip().split()))
            e_count[e_id] = cover_count
            for id in cover_ids:
                cover[id].append(e_id)

    return n, m, cover, e_count

"""遗传算法"""
def greedy_cover(cover, e_counts, n, m):
    e_covered = set()
    selected = []

    while len(e_covered) < n:
        new = 0
        best = None

        for set_id, covered_ine in cover.items():
            uncovered = set(covered_ine) - e_covered
            if len(uncovered) > new and set_id not in selected:
                new = len(uncovered)
                best = set_id

        if best is None:
            print("无法进一步覆盖剩余采样点")
            break

        selected.append(best)
        e_covered.update(cover[best])

    return selected, e_covered

"""检查方法，解题可以不用"""
def check(solution, cover, n):
    new = []
    dict = {}
    missing = []
    for i in solution:
        value = cover[i]
        new.extend(value)
        for num in value:
            dict[num] = dict.get(num, 0) + 1

    for num in range(0, n):
        if num not in dict:
            missing.append(num)

    repeated_ids = [num for num, count in dict.items() if count > 1]

    return repeated_ids, missing

"""主函数"""
def main():
    input_file = r'D:\桌面\大二\数据结构2\SetCoveringTestData\Test05.txt'
    n, m, cover, _ = read_input(input_file)
    solution, _ = greedy_cover(cover, [0] * n, n, m)

    print(len(solution))
    print(*solution)
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
