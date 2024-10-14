import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] # 用黑体显示中文
plt.rcParams['axes.unicode_minus']=False # 正常显示负号
# 给定条件
p0 = 0.10  # 标称次品率
alpha = 0.05  # 第一类错误的概率，即当批质量差时仍接受批的概率
beta = 0.10   # 第二类错误的概率，即当批质量好时仍拒收批的概率

# 寻找合适的样本大小n和最大允许不合格品数量c
def find_acceptance_plan(p0, alpha, beta):
    n = 196  # 初始样本大小
    while True:
        c = binom.ppf(1 - alpha, n, p0)  # 计算最大允许的不合格品数量c
        if binom.cdf(c, n, p0) >= 1 - beta:  # 检查当p <= p0时批被接受的概率是否至少为1-beta
            break
    return n, c

def calculate_oc_curve(n, c, p_r=np.linspace(0, 0.2, 100)):
    oc_v = [binom.cdf(c, n, p) for p in p_r]
    return p_r, oc_v

n, c = find_acceptance_plan(p0, alpha, beta)

p_range, oc_values = calculate_oc_curve(n, c)

plt.figure(figsize=(10, 6))
plt.plot(p_range, oc_values, label='OC 曲线')
plt.axvline(x=p0, color='r', linestyle='--', label=f'p0={p0}')
plt.xlabel('标称值')
plt.ylabel('验收率')
plt.title(f'样本容量为{n}且接受的临界值为{c}时OC方法检验下的验收率')
plt.legend()
plt.grid(True)
plt.show()

print(f"Sample size (n): {n}")
print(f"Acceptance number (c): {c}")

print("------------------")
n, c = find_acceptance_plan(p0, alpha, beta)

def simulate_dqa(p, n, c, num_simulations=10000):
    accepted = 0
    for _ in range(num_simulations):
        defects = binom.rvs(n=n, p=p)
        if defects <= c:
            accepted += 1
    return accepted / num_simulations

p_v = np.linspace(0, 0.2, 100)
acceptance_r = [simulate_dqa(p, n, c) for p in p_v]

plt.figure(figsize=(10, 6))
plt.plot(p_v, acceptance_r, label='DQA 验收率')
plt.axvline(x=p0, color='r', linestyle='--', label=f'p0={p0}')
plt.xlabel('标称值')
plt.ylabel('验收率')
plt.title(f'样本容量为{n}且接受的临界值为{c}时DQA方法检验下的验收率')
plt.legend()
plt.grid(True)
plt.show()