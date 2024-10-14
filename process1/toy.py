import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR


# 创建玩具数据集
X = np.sort(5 * np.random.rand(200, 1), axis=0)
y = np.sin(X).ravel()

# 给目标变量添加噪声
y += 0.2 * np.random.randn(len(X))

# 使用不同核函数的支持向量机进行回归
kernels = ['linear', 'poly', 'rbf']
colors = ['r', 'g', 'b']

for kernel, color in zip(kernels, colors):
    # 创建 SVR 回归模型对象
    svr = SVR(kernel=kernel)

    # 在训练集上训练模型
    svr.fit(X, y)

    # 在连续范围内生成预测结果
    X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    y_pred = svr.predict(X_test)

    # 绘制训练数据点和预测曲线
    plt.scatter(X, y, color=color, label='Training Data')
    plt.plot(X_test, y_pred, color=color, linewidth=2, label=f'{kernel.capitalize()} Kernel')

plt.xlabel('X')
plt.ylabel('y')
plt.title('SVR Regression with Different Kernels')
plt.legend()
plt.show()
