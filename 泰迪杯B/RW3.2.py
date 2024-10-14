import numpy as np
from sklearn import metrics

def linear_regression(X, y):
    # 添加常数项（截距），并使其服从正态分布
    X = np.column_stack((np.random.normal(size=X.shape[0]), X))

    # 计算设计矩阵的转置和乘积
    XTX = np.dot(X.T, X)
    XTy = np.dot(X.T, y)

    # 解线性方程组以获取系数
    beta = np.linalg.solve(XTX, XTy)


    return beta

# 读取数据
data = np.loadtxt('LR_new.txt')
X = data[:, :-1]
y = data[:, -1]

# 训练模型
coefficients = linear_regression(X, y)

# 打印模型的系数
print('Coefficients:', coefficients[1:])

# 使用模型进行预测
y_pred = np.dot(np.column_stack((np.ones(X.shape[0]), X)), coefficients)

# 计算并打印模型的性能指标
print('Mean Absolute Error:', metrics.mean_absolute_error(y, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, y_pred)))