import threading
import time

class FamilyDinner:
    def __init__(self):
        self.dish = None
        self.lock = threading.Lock()
        self.apple_condition = threading.Condition(self.lock)
        self.orange_condition = threading.Condition(self.lock)

    def put_apple(self):
        with self.apple_condition:
            while self.dish is not None:
                self.apple_condition.wait()
            self.dish = 'apple'
            print("爸爸放了一个苹果在盘子里。")
            self.orange_condition.notify()  # 唤醒吃桔子的女儿

    def put_orange(self):
        with self.orange_condition:
            while self.dish is not None:
                self.orange_condition.wait()
            self.dish = 'orange'
            print("妈妈放了一个桔子在盘子里。")
            self.apple_condition.notify()  # 唤醒吃苹果的儿子

    def eat_apple(self):
        with self.apple_condition:
            while self.dish != 'apple':
                self.apple_condition.wait()
            self.dish = None
            print("儿子吃了苹果。")
            self.orange_condition.notify()  # 唤醒放桔子的妈妈

    def eat_orange(self):
        with self.orange_condition:
            while self.dish != 'orange':
                self.orange_condition.wait()
            self.dish = None
            print("女儿吃了桔子。")
            self.apple_condition.notify()  # 唤醒放苹果的爸爸

def main():
    dinner = FamilyDinner()

    father = threading.Thread(target=lambda: [dinner.put_apple(), time.sleep(1)], daemon=True)
    mother = threading.Thread(target=lambda: [dinner.put_orange(), time.sleep(1)], daemon=True)
    son = threading.Thread(target=lambda: [dinner.eat_apple(), time.sleep(1)], daemon=True)
    daughter = threading.Thread(target=lambda: [dinner.eat_orange(), time.sleep(1)], daemon=True)

    father.start()
    mother.start()
    son.start()
    daughter.start()

    # 让主线程等待子线程
    time.sleep(10)

if __name__ == "__main__":
    main()