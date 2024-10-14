import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV
import matplotlib.pyplot as plt
import seaborn as sns


# 读取数据
df = pd.read_csv("financial_data.csv")

# 提取自变量和因变量
X = df[['YYSR', 'YWFY', 'YYCB', 'YYSJJFJ', 'ZCJZSS']]
y = df['LRZE']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化LassoCV模型
model = LassoCV(cv=5)

# 拟合模型
model.fit(X_train, y_train)

# 输出最佳的lambda值
print("Best alpha using built-in LassoCV: %f" % model.alpha_)

# 生成交叉验证图
m_log_alphas = -np.log10(model.alphas_)
plt.figure()
plt.plot(m_log_alphas, model.mse_path_, ':')
plt.plot(m_log_alphas, model.mse_path_.mean(axis=-1), 'k', label='Average across the folds', linewidth=2)
plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k', label='alpha: CV estimate')
plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('Mean square error')
plt.title('Mean square error on each fold: coordinate descent')
plt.show()

# 输出模型的回归系数
coefs = pd.Series(model.coef_, index=X.columns)
print("Lasso picked " + str(sum(coefs != 0)) + " variables and eliminated the other " + str(sum(coefs == 0)) + " variables")

colors = sns.color_palette("bright", len(coefs))

plt.figure()
barplot = coefs.plot(kind='bar', color=colors, edgecolor='black', linewidth=1)  # 增加边框线条
plt.title('Model Coefficients')
plt.show()
# 输出模型系数表
print(coefs)

# 预测结果
y_pred = model.predict(X_test)

# 绘制模型结果图
plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.title('True Values vs Predictions')
plt.show()
