import pandas as pd
import numpy as np
import random


# 生成随机职业数据
occupations = ["数据分析师", "数据分析师", "人工智能工程师", "人工智能工程师", "软件工程师", "电子商务专家",
               "前端工程师", "后端工程师", "机器学习工程师", "机器学习工程师"]
occupations = occupations + ["软件工程师", "后端工程师"]  # 数据分析师，人工智能工程师的总数量比其他多
occupations = occupations + ["机器学习工程师"]  # 机器学习工程师的总数量比其他少

# 生成随机地区数据
provinces = ["北京","北京", "上海", "上海","广东","广东","广东","广东","江苏","江苏", "江苏", "浙江","浙江", "浙江","浙江","福建","福建", "山东", "山东","广西", "海南", "天津", "辽宁",
             "吉林", "黑龙江", "河北",  "河北", "山西", "内蒙古", "河南", "湖北", "湖南", "湖北", "湖南","重庆", "四川","四川",
             "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆", "安徽","安徽","安徽",  "江西","江西"]

# 生成技能数据
skills = ["Python",  "Python" , "Java", "Java", "C++", "C++", "TensorFlow", "PyTorch", "SQL", "Ruby", "Node.js", "C", "PHP", "React"]

data = []
for i in range(300000):
    occupation = random.choice(occupations)
    province = random.choice(provinces)  # 随机选择省份
    main_skill, sub_skill1, sub_skill2 = random.sample(skills, 3)

    # 根据月份调整投简历数据量
    if np.random.choice([True, False], p=[0.4, 0.6]):
        resume_month = np.random.randint(1, 7)  # 1-6月份数据量较多
    else:
        resume_month = np.random.randint(7, 13)  # 7-12月份数据量较多

    data.append({"id": i + 1, "职业": occupation, "地区": province,
                 "主要技能": main_skill, "次要技能1": sub_skill1, "次要技能2": sub_skill2, "投简历月份": resume_month})

df = pd.DataFrame(data)
df.to_excel(r'D:\桌面\竞赛\服务外包\服务外包测试数据.xlsx', index=False)
