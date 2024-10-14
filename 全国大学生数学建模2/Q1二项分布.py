import scipy.stats as stats
import numpy as np


confidence_level_reject = 0.95
confidence_level_accept = 0.90
defect_rate_claimed = 0.10

def calculate_sample_size_reject(confidence, defect_rate):

    z_score = stats.norm.ppf(1 - (1 - confidence) / 2)
    n = ((z_score ** 2 * defect_rate * (1 - defect_rate)) /
         ((defect_rate - 0.1) ** 2))
    return int(np.ceil(n))

def calculate_sample_size_accept(confidence, defect_rate):

    z_score = stats.norm.ppf(confidence)
    n = ((z_score ** 2 * defect_rate * (1 - defect_rate)) /
         ((0.1 - defect_rate) ** 2))
    return int(np.ceil(n))

# 计算临界值c
def calculate_critical_value(n, confidence, defect_rate):
    c = stats.binom.ppf(confidence, n, defect_rate)
    return min(c, n)

np.random.seed(42)

n_reject = calculate_sample_size_reject(confidence_level_reject, defect_rate_claimed + 0.05)
c_reject = calculate_critical_value(n_reject, confidence_level_reject, defect_rate_claimed + 0.05)

n_accept = calculate_sample_size_accept(confidence_level_accept, defect_rate_claimed - 0.05)
c_accept = calculate_critical_value(n_accept, confidence_level_accept, defect_rate_claimed - 0.05)

print(f"在{confidence_level_reject*100}%的置信水平下拒绝次品率大于10%的样本大小为: {n_reject}, 临界值为: {c_reject}")
print(f"在{confidence_level_accept*100}%的置信水平下接受次品率小于等于10%的样本大小为: {n_accept}, 临界值为: {c_accept}")