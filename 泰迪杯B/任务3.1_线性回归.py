import pandas as pd
from spsspro.algorithm import statistical_model_analysis


# 读取数据表
df = pd.read_csv(r"D:\桌面\financial_data.csv")

# 选择自变量和因变量
data_x1 = df[["YYSR", "YWFY", "YYCB", "YYSJJFJ", "ZcJZsS"]]
data_y = df["LRZE"]

# 线性回归
result = statistical_model_analysis.linear_regression(data_y=data_y, data_x1=data_x1)
print(result)
