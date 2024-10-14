import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 加载数据
df = pd.read_excel('data.xlsx')

# 定义特征和目标变量
X = df[['老年人口数', '比重', '老年抚养比', '享受老年人补贴']]
y = df['床位数']

# 创建线性回归模型
model = LinearRegression()
model.fit(X, y)

# 输出拟合函数
print("拟合函数：y =", model.intercept_, "+", model.coef_[0], "* x1 +", model.coef_[1], "* x2 +", model.coef_[2], "* x3 +", model.coef_[3], "* x4")


# 预测新数据
predictions = model.predict(X)

# 计算评估指标
mse = mean_squared_error(y, predictions)
r2 = r2_score(y, predictions)

print("\n评估指标：")
print("均方误差 (MSE)：", mse)
print("R^2 分数：", r2)