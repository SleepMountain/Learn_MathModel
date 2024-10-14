import pandas as pd
from spsspro.algorithm import supervised_learning

# 读取训练数据和预测数据
train_data = pd.read_csv(r"D:\桌面\financial_data.csv")
test_data = pd.read_csv(r"D:\桌面\financial_data_new.csv")

# 选择训练数据的自变量和因变量
train_x = train_data[["YYSR", "YWFY", "YYCB", "YYSJJFJ", "ZcJZsS"]]
train_y = train_data["LRZE"]

# 训练逻辑回归模型
result = supervised_learning.logistic_regression(data_x=train_x, data_y=train_y)

# 选择预测数据的自变量
test_x = test_data[["YYSR", "YWFY", "YYCB", "YYSJJFJ", "ZcJZsS"]]

# 使用训练好的模型进行预测
test_data["LRZE_prediction"] = result.predict(test_x)

# 输出预测结果
print(test_data[["YYSR", "YWFY", "YYCB", "YYSJJFJ", "ZcJZsS", "LRZE_prediction"]])
