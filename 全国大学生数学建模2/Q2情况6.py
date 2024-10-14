import random


PART1_PRICE = 4
PART1_INSPECT_COST = 2
PART1_DEFECT_RATE = 0.05

PART2_PRICE = 18
PART2_INSPECT_COST = 3
PART2_DEFECT_RATE = 0.05

PRODUCT_ASSEMBLY_COST = 6
PRODUCT_INSPECT_COST = 3
PRODUCT_DEFECT_RATE = 0.05

PRODUCT_MARKET_PRICE = 56
PRODUCT_REPLACEMENT_LOSS = 10
DISASSEMBLE_COST = 40

strategies = [
    [1, 1, 1, 1],
    [1, 1, 1, 0],
    [1, 1, 0, 1],
    [1, 1, 0, 0],
    [1, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 1, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
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
            if self.detect_part1:
                part1_cost = PART1_PRICE + PART1_INSPECT_COST
            else:
                part1_cost = PART1_PRICE * (1 - PART1_DEFECT_RATE)
            part1 = random.random() > PART1_DEFECT_RATE

            if self.detect_part2:
                part2_cost = PART2_PRICE + PART2_INSPECT_COST
            else:
                part2_cost = PART2_PRICE * (1 - PART2_DEFECT_RATE)
            part2 = random.random() > PART2_DEFECT_RATE

            if not part1 or not part2:
                continue

            total_cost += PRODUCT_ASSEMBLY_COST

            if self.detect_product:
                if random.random() < PRODUCT_DEFECT_RATE:
                    defective_products += 1
                    if self.disassemble:
                        total_cost += DISASSEMBLE_COST
                        part1_cost, part2_cost = PART1_PRICE + PART1_INSPECT_COST, PART2_PRICE + PART2_INSPECT_COST
                        if part1 and part2:
                            total_cost -= (PART1_PRICE + PART2_PRICE)
                    continue
                else:
                    total_cost += PRODUCT_INSPECT_COST
            else:
                if random.random() < PRODUCT_DEFECT_RATE:
                    defective_products += 1

            sold_products += 1
            total_revenue += PRODUCT_MARKET_PRICE

        total_cost += defective_products * PRODUCT_REPLACEMENT_LOSS

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
