import random

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

    return n, m, cover

def fitness(sets, cover, n):
    covered_e = set()
    for s in sets:
        covered_e.update(cover[s])
    return len(covered_e), covered_e

def select(population, fitnesses, elite_size):
    sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1][0], reverse=True)
    return [ind for ind, fit in sorted_population[:elite_size]]

def crossover(parent1, parent2):
    return parent1[:len(parent1)//2] + parent2[len(parent2)//2:]

def mutate(individual, mutation_rate, m):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, m-1)
    return individual

def genetic_algorithm(cover, n, m, pop_size=50, generations=100, elite_size=10, mutation_rate=0.05):
    population = [random.sample(range(m), pop_size) for _ in range(pop_size)]
    best_solution = None
    best_fitness = 0

    for gen in range(generations):
        fitnesses = [fitness(ind, cover, n) for ind in population]
        population = select(population, fitnesses, elite_size)
        while len(population) < pop_size:
            parent1, parent2 = random.sample(population, 2)
            offspring1, offspring2 = crossover(parent1, parent2), crossover(parent2, parent1)
            offspring1 = mutate(offspring1, mutation_rate, m)
            offspring2 = mutate(offspring2, mutation_rate, m)
            population.extend([offspring1, offspring2])

        now_best_fitness, _ = fitness(population[0], cover, n)
        if now_best_fitness > best_fitness:
            best_fitness = now_best_fitness
            best_solution = population[0]

    return best_solution, best_fitness

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

def main(input_file):
    n, m, cover = read_input(input_file)
    solution, covered_samples = genetic_algorithm(cover, n, m)
    print(len(solution))
    print(*solution)
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