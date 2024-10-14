import pandas as pd
import random


# 生成工作省份数据
provinces = ["北京", "上海",  "广东", "浙江", "江苏", "福建", "山东", "安徽", "江西"]
work_provinces = [random.choice(provinces) for _ in range(100)]

# 生成职位数据
positions = ["数据分析师", "数据分析师", "人工智能工程师", "人工智能工程师", "软件工程师", "电子商务专家", "前端工程师", "后端工程师", "机器学习工程师", "机器学习工程师"]
jobs = [random.choice(positions) for _ in range(100)]

# 生成满意度数据
satisfactions = [5] * int(0.85 * 100) + [4] * int(0.1 * 100) + [3] * int(0.03 * 100) + [2] * int(0.02 * 100)
random.shuffle(satisfactions)

# 生成易操作性数据
ease_of_use = [5] * int(0.95 * 100) + [4] * int(0.05 * 100)
random.shuffle(ease_of_use)

# 创建 DataFrame
data = {
    "id": range(1, 101),
    "工作省份": work_provinces,
    "职位": jobs,
    "满意度": satisfactions,
    "易操作性": ease_of_use
}

df = pd.DataFrame(data)

# 将 DataFrame 写入 Excel 文件
df.to_excel("D:/桌面/竞赛/服务外包/问卷调查3.xlsx", index=False)
