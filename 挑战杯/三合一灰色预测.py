import numpy as np
import matplotlib.pyplot as plt


# 定义灰色预测函数
def GM11(x0):
    x1 = np.cumsum(x0)
    z1 = (x1[:-1] + x1[1:]) / 2.0
    B = np.array([[-z1[i], 1] for i in range(len(z1))])
    Y = x0[1:].reshape((len(x0) - 1, 1))
    u = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Y)
    a, b = u.flatten()
    x_pred = np.zeros(len(x0))
    x_pred[0] = x0[0]
    for i in range(1, len(x0)):
        x_pred[i] = (x0[0] - b / a) * np.exp(-a * (i - 1)) - (x0[0] - b / a) * np.exp(-a * i)
    return x_pred


# 数据
year = [2016, 2017, 2018, 2019, 2020, 2021]
market_size_domestic = [42, 59.8, 80, 78.2, 86, 115.6]
market_size_global = [2739.4, 3336.6, 4047, 4389.8, 5269.7, 6191.6]
market_size_new_energy = [6503, 7705, 8823, 9075, 9335, 10399]

# 灰色预测
n = 5  # 预测年数
x_domestic_pred = GM11(np.array(market_size_domestic))
x_global_pred = GM11(np.array(market_size_global))
x_new_energy_pred = GM11(np.array(market_size_new_energy))
for i in range(n):
    x_domestic_pred = np.append(x_domestic_pred,
                                (x_domestic_pred[-1] - x_domestic_pred[-2]) * np.exp(-0.5355) + x_domestic_pred[-1])
    x_global_pred = np.append(x_global_pred,
                              (x_global_pred[-1] - x_global_pred[-2]) * np.exp(-0.4633) + x_global_pred[-1])
    x_new_energy_pred = np.append(x_new_energy_pred,
                                  (x_new_energy_pred[-1] - x_new_energy_pred[-2]) * np.exp(-0.3863) + x_new_energy_pred[-1])

# 输出未来五年三个指标的值
print("未来五年预测值：")
print("国内扫地机市场规模：", x_domestic_pred[-5:])
print("全球扫地机器人市场规模：", x_global_pred[-5:])
print("中国新能源市场规模统计：", x_new_energy_pred[-5:])

# 绘制折线图
plt.plot(year, market_size_domestic, 'o-', label='国内扫地机市场规模')
plt.plot(year, market_size_global, 'o-', label='全球扫地机器人市场规模')
plt.plot(year, market_size_new_energy, 'o-', label='中国新能源市场规模统计')
plt.plot(range(2016, 2027), x_domestic_pred, 'x-', label='国内扫地机市场规模预测')
plt.plot(range(2016, 2027), x_global_pred, 'x-', label='全球扫地机器人市场规模预测')
plt.plot(range(2016, 2027), x_new_energy_pred, 'x-', label='中国新能源市场规模统计预测')
plt.legend(loc='best')
plt.xlabel('年份')
plt.ylabel('市场规模')
plt.show()
