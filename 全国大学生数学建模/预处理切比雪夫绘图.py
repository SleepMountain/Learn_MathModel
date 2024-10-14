import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_excel('D:\桌面\数据表\数据预处理切比雪夫数据表.xlsx')

x = data.iloc[:, 0]
y = data.iloc[:, 1]

plt.figure()
plt.xlabel("X")
plt.ylabel("Y")

colors = ['r' if val > 8 else 'b' for val in y]

plt.scatter(x, y, color=colors)

plt.show()
