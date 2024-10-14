import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# 读取数据表，跳过第一行，只选择前五列数据
data = pd.read_excel('D:\桌面\竞赛\数模\暑假训练\progress3\热熔3.xlsx', usecols=[0, 1, 2, 3, 4])

# 假设接收距离、热风速度、厚度和孔隙率为自变量，压缩回弹性率为因变量
X = data[['接收距离(cm)', '热风速度(r/min)', '厚度mm', '孔隙率（%）']]
y = data['压缩回弹性率（%）']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# 创建线性回归模型
model = LinearRegression()
# 在训练集上拟合模型
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print('均方误差:', mse)

# 打印回归系数和截距
print('回归系数:', model.coef_)
print('截距:', model.intercept_)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print('均方误差:', mse)