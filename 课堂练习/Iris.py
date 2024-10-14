from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# 加载鸢尾花数据集
iris = load_iris()


# 特征矩阵
X = iris.data
# 标签向量
y = iris.target

# 数据集划分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 特征缩放
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 使用不同核函数的支持向量机模型
kernels = ['linear', 'poly', 'rbf', 'sigmoid']

for kernel in kernels:
    # 创建 SVM 分类器对象
    svm = SVC(kernel=kernel)

    # 在训练集上训练模型
    svm.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = svm.predict(X_test)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)

    # 输出结果
    print(f"使用 {kernel} 核函数的 SVM 模型准确率：{accuracy}")
