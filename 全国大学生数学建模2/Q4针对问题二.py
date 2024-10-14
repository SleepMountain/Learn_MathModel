import random
import numpy as np
import scipy.stats as stats


def normal_sampling(mean, std_dev, size=1):
    return np.random.normal(loc=mean, scale=std_dev, size=size)

def fitness_function(decision, components, product):
    total_savings = 0
    total_cost = 0
    total_inspection = 0
    total_defect = 0

    for i, comp in enumerate(components):
        sampled_defect_rate = max(0, normal_sampling(comp['defect_rate'], comp['defect_rate'] * 0.1))
        if decision[i]:
            total_savings += comp['cost'] * sampled_defect_rate
            total_cost += comp['inspect_cost']
            total_inspection += 1
        else:
            total_cost += comp['cost'] * sampled_defect_rate
            total_defect += 1

    product_start = len(components)
    sampled_defect_rate = max(0, normal_sampling(product['defect_rate'], product['defect_rate'] * 0.1))
    if decision[product_start]:
        total_savings += product['assembly_cost'] * sampled_defect_rate
        total_cost += product['inspect_cost']
        total_inspection += 1
    else:
        total_cost += product['assembly_cost'] * sampled_defect_rate
        total_defect += 1

    profit = product['sale_price'] - total_cost - product['replacement_loss'] + total_savings

    fitness = total_savings - total_cost + abs(total_cost)
    return fitness, profit, total_inspection, total_defect

def calculate_sample_size(confidence, aql=0.1, power=0.9):
    z_alpha = stats.norm.ppf(1 - (1 - confidence) / 2)
    z_beta = stats.norm.ppf(power)
    p = aql
    delta = aql
    n = (z_alpha * np.sqrt(p * (1 - p)) + z_beta * np.sqrt((p + delta) * (1 - (p + delta)))) ** 2 / (delta ** 2)
    return int(np.ceil(n))

CONFIDENCE_95 = 0.95
CONFIDENCE_90 = 0.90
AQL = 0.1

N_95 = calculate_sample_size(CONFIDENCE_95, AQL)
N_90 = calculate_sample_size(CONFIDENCE_90, AQL)

#情况1
PART1 = {'cost': 4, 'inspect_cost': 2, 'defect_rate': 0.1}
PART2 = {'cost': 18, 'inspect_cost': 3, 'defect_rate': 0.1}
PRODUCT = {'assembly_cost': 6, 'inspect_cost': 3, 'sale_price': 56, 'replacement_loss': 6, 'defect_rate': 0.1}
DISASSEMBLE_COST = 5

"""
情况2
PART1 = {'cost': 4, 'inspect_cost': 2, 'defect_rate': 0.2}
PART2 = {'cost': 18, 'inspect_cost': 3, 'defect_rate': 0.2}
PRODUCT = {'assembly_cost': 6, 'inspect_cost': 3, 'sale_price': 56, 'replacement_loss': 6, 'defect_rate': 0.2}
DISASSEMBLE_COST = 5  
"""

"""
# 情况3
PART1 = {'cost': 4, 'inspect_cost': 2, 'defect_rate': 0.1}
PART2 = {'cost': 18, 'inspect_cost': 3, 'defect_rate': 0.1}
PRODUCT = {'assembly_cost': 6, 'inspect_cost': 3, 'sale_price': 56, 'replacement_loss': 30, 'defect_rate': 0.1}
DISASSEMBLE_COST = 5 
"""

"""
# 情况4
PART1 = {'cost': 4, 'inspect_cost': 1, 'defect_rate': 0.2}
PART2 = {'cost': 18, 'inspect_cost': 1, 'defect_rate': 0.2}
PRODUCT = {'assembly_cost': 6, 'inspect_cost': 2, 'sale_price': 56, 'replacement_loss': 30, 'defect_rate': 0.2}
DISASSEMBLE_COST = 5  
"""

"""
# 情况5
PART1 = {'cost': 4, 'inspect_cost': 8, 'defect_rate': 0.1}
PART2 = {'cost': 18, 'inspect_cost': 1, 'defect_rate': 0.2}
PRODUCT = {'assembly_cost': 6, 'inspect_cost': 2, 'sale_price': 56, 'replacement_loss': 10, 'defect_rate': 0.1}
DISASSEMBLE_COST = 5 
"""

"""
# 情况6
PART1 = {'cost': 4, 'inspect_cost': 2, 'defect_rate': 0.05}
PART2 = {'cost': 18, 'inspect_cost': 3, 'defect_rate': 0.05}
PRODUCT = {'assembly_cost': 6, 'inspect_cost': 3, 'sale_price': 56, 'replacement_loss': 10, 'defect_rate': 0.05}
DISASSEMBLE_COST = 40 
"""

components = [PART1, PART2]

strategies = [
    [1, 1, 1, 1],  # 检测所有
    [1, 1, 1, 0],  # 不拆解
    [1, 1, 0, 1],  # 不检测成品
    [1, 1, 0, 0],  # 不检测成品和不拆解
    [1, 0, 1, 1],  # 不检测零配件2
    [1, 0, 1, 0],  # 不检测零配件2和不拆解
    [1, 0, 0, 1],  # 不检测零配件2和成品
    [1, 0, 0, 0],  # 不检测零配件2、成品和不拆解
    [0, 1, 1, 1],  # 不检测零配件1
    [0, 1, 1, 0],  # 不检测零配件1和不拆解
    [0, 1, 0, 1],  # 不检测零配件1和成品
    [0, 1, 0, 0],  # 不检测零配件1、成品和不拆解
    [0, 0, 1, 1],  # 仅检测成品
    [0, 0, 1, 0],  # 仅检测成品且不拆解
    [0, 0, 0, 1],  # 不检测任何
    [0, 0, 0, 0]   # 不检测任何且不拆解
]

class ProductAssembly:
    def __init__(self, detect_part1, detect_part2, detect_product, disassemble):
        self.detect_part1 = detect_part1
        self.detect_part2 = detect_part2
        self.detect_product = detect_product
        self.disassemble = disassemble

    def simulate(self, num_products=1000):
        total_cost = 0
        total_revenue = 0
        sold_products = 0
        defective_products = 0

        for _ in range(num_products):
            part1_defect = random.random() < PART1['defect_rate']
            part2_defect = random.random() < PART2['defect_rate']

            if part1_defect:
                part1_cost = PART1['cost'] + PART1['inspect_cost'] if self.detect_part1 else PART1['cost']
            else:
                part1_cost = 0

            if part2_defect:
                part2_cost = PART2['cost'] + PART2['inspect_cost'] if self.detect_part2 else PART2['cost']
            else:
                part2_cost = 0

            if part1_defect or part2_defect:
                total_cost += part1_cost + part2_cost
                if self.disassemble:
                    total_cost += DISASSEMBLE_COST
                    total_cost -= (PART1['cost'] + PART2['cost'])
                continue

            total_cost += PRODUCT['assembly_cost']

            if self.detect_product:
                if random.random() < PRODUCT['defect_rate']:
                    defective_products += 1
                    if self.disassemble:
                        total_cost += DISASSEMBLE_COST
                        total_cost -= (PART1['cost'] + PART2['cost'])
                    continue
                else:
                    total_cost += PRODUCT['inspect_cost']
            else:
                if random.random() < PRODUCT['defect_rate']:
                    defective_products += 1

            sold_products += 1
            total_revenue += PRODUCT['sale_price']

        total_cost += defective_products * PRODUCT['replacement_loss']

        return total_cost, total_revenue, sold_products, defective_products

num_products = 1000
for strategy in strategies:
    detect_part1, detect_part2, detect_product, disassemble = strategy
    assembly = ProductAssembly(detect_part1, detect_part2, detect_product, disassemble)
    cost, revenue, sold_products, defective_products = assembly.simulate(num_products=num_products)
    profit = revenue - cost
    print(f"策略 {strategy}:")
    print(f"  成本={cost:.2f}, 收入={revenue:.2f}, 净利润={profit:.2f}")
    print(f"  销售产品数量={sold_products}, 次品数量={defective_products}")
    print(f"  总产品数量={num_products}\n")