import threading
import random
import time



class Supplier(threading.Thread):
    def __init__(self, table):
        super().__init__()
        self.table = table

    def run(self):
        while True:
            # 选择两种材料
            materials = random.sample(['烟草', '纸', '火柴'], 2)
            print(f"供应者在桌上放置了 {materials}.")
            self.table.place_materials(materials)

class Smoker(threading.Thread):
    def __init__(self, name, material, table):
        super().__init__()
        self.name = name
        self.material = material
        self.table = table

    def run(self):
        while True:
            self.table.take_material(self.material, self.name)

class SmokingTable:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.materials_on_table = []

    def place_materials(self, materials):
        with self.condition:
            self.materials_on_table.extend(materials)
            self.condition.notify_all()

    def take_material(self, owned_material, smoker_name):
        with self.condition:
            while len(set(self.materials_on_table) - {owned_material}) < 2:
                self.condition.wait()

            self.materials_on_table.remove(owned_material)
            other_material = set(self.materials_on_table) - {owned_material}
            self.materials_on_table.remove(list(other_material)[0])

            print(f"{smoker_name} 拿走了 {owned_material} 和 {list(other_material)[0]} 从桌上.")
            # 模拟吸烟所需的时间
            time.sleep(1)
            print(f"{smoker_name} 在吸烟.")


if __name__ == "__main__":
    table = SmokingTable()

    smokers = [
        Smoker('Smoker 1', '烟草', table),
        Smoker('Smoker 2', '纸', table),
        Smoker('Smoker 3', '火柴', table)
    ]

    for smoker in smokers:
        smoker.start()

    Supplier(table).start()