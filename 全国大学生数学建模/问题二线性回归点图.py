import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel(r"D:\桌面\数据表\线性回归点图示意数据（以花叶类为例）.xlsx")

x = df.iloc[:, 0]
y = df.iloc[:, 1]

plt.scatter(x, y)
plt.show()