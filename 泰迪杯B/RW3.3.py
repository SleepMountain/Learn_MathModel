import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 定义逻辑回归类
class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None


    def fit(self, X, y):
        n_samples, n_features = X.shape

        # 初始化权重和偏置
        self.weights = np.zeros(n_features)
        self.bias = 0

        # 训练模型
        for _ in range(self.n_iters):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self._sigmoid(linear_model)

            # 计算梯度
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)

            # 更新权重和偏置
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self._sigmoid(linear_model)
        y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
        return y_predicted_cls

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

# 加载数据
df = pd.read_csv('LR_new3.csv')
# 定义特征和目标变量
features = ['LDBL', 'ZCFZL', 'CHZZL', 'ZCBCL', 'YSZKZZL']
target = 'is_fraud'
# 将目标变量转换为二进制（0表示非造假，1表示造假）
df[target] = df[target].apply(lambda x: 1 if x == '造假' else 0)
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split\
    (df[features], df[target], test_size=0.2, random_state=42)
# 数据预处理：标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 训练逻辑回归模型
lr = LogisticRegression()
lr.fit(X_train, y_train)

# 预测测试集
y_pred = lr.predict(X_test)

# 找出预测为造假的数据并标记为0
df.loc[df.index.isin(X_test.index[y_pred == 1]), 'is_fraud'] = 0

# 输出结果
print(df)