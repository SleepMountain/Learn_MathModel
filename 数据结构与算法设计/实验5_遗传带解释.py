import random

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
                cover[id].append(e_id)

    return n, m, cover

"""计算给定一组sets能够覆盖的所有采样点"""
def fitness(sets, cover, n):                                             # 列表，字典，总数
    covered_e = set()                                                    # 存储被当且set覆盖的采样点
    for s in sets:
        covered_e.update(cover[s])                                       # 合并所有集合能覆盖的采样点（保证只被计算一次）
    return len(covered_e), covered_e

"""选择出最优秀的个体形成一个新的种群"""
def select(population, fitnesses, elite_size):                           # 个体集合和对应个体的适应度集合配对,输出适应度最高的个体
    sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1][0], reverse=True)
    return [ind for ind, fit in sorted_population[:elite_size]]

"""交叉操作"""
def crossover(parent1, parent2):                                         # 通过取parent1的前半部分和parent2的后半部分,新生个体
    return parent1[:len(parent1)//2] + parent2[len(parent2)//2:]

"""随机变异"""
def mutate(individual, mutation_rate, m):                                # 变异目标，变异率，上限
    for i in range(len(individual)):                                     # 对个体中的每个基因位置进行迭代
        if random.random() < mutation_rate:                              # 是否变异
            individual[i] = random.randint(0, m-1)                       # 随机赋予整数
    return individual

"""遗传算法"""
def genetic_algorithm(cover, n, m, pop_size=50, generations=100, elite_size=10, mutation_rate=0.045):
    population = [random.sample(range(m), pop_size) for _ in range(pop_size)]
    best_solution = None                                                 # 初始化种群（随机索引）/最佳解/最佳适应度值
    best_fitness = 0

    for gen in range(generations):                                       # 迭代
        fitnesses = [fitness(ind, cover, n) for ind in population]       # 计算当前种群中每个个体的适应度（即覆盖效率或满足条件的程度）
        population = select(population, fitnesses, elite_size)           # 选择操作，根据适应度保留elite_size个最佳个体到下一代种群
        while len(population) < pop_size:                                # 当种群数量小于初始大小时，进行繁殖补充
            parent1, parent2 = random.sample(population, 2)              # 随机选择两个不同的父代进行交叉操作
            offspring1, offspring2 = crossover(parent1, parent2), crossover(parent2, parent1)
            offspring1 = mutate(offspring1, mutation_rate, m)            # 子代1变异
            offspring2 = mutate(offspring2, mutation_rate, m)            # 子代2变异
            population.extend([offspring1, offspring2])                  # 子代回归种群

        now_best_fitness, _ = fitness(population[0], cover, n)           # 计算当前代最优秀个体的适应度，并判断是否优于已知的最佳解
        if now_best_fitness > best_fitness:
            best_fitness = now_best_fitness
            best_solution = population[0]

    return best_solution, best_fitness

"""检查函数"""
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
def main(input_file):
    n, m, cover = read_input(input_file)
    solution, covered_samples = genetic_algorithm(cover, n, m)
    print(len(solution))                                                  # 输出选中的候选机位数量
    print(*solution)                                                      # 输出选中的候选机位
    # print("\n选中的集合包含的采样点：")
    # for set_id in solution:
    #     print(f"集合{set_id}: {cover[set_id]}")

    repeated_ids, missing = check(solution, cover, n)
    print("\n验证结果：")
    print(f"重复覆盖的采样点数量: {len(repeated_ids)}")
    print(f"未覆盖的采样点数量: {len(missing)}")
    # print(f"重复覆盖的采样点数量: {len(repeated_ids)}, 重复的采样点: {repeated_ids}")
    # print(f"未覆盖的采样点数量: {len(missing)}, 未覆盖的采样点: {missing}")

if __name__ == '__main__':
    main(r'D:\桌面\大二\数据结构2\SetCoveringTestData\Test05.txt')