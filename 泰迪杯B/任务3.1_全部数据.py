import pandas as pd

# 读取数据
df = pd.read_csv("D:\桌面\\financial_data.csv")

# 计算相关性
correlation = df.corr()['LRZE'].sort_values(ascending=False)

# 输出所有指标对应的相关度
print(correlation)


# 输出所有指标对应的相关度到 Excel 表格
correlation.to_excel("D:\桌面\correlation_results.xlsx")
