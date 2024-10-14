import numpy as np
import scipy.stats as stats


def calculate_sample_size(confidence, aql=0.1, power=0.9):
    z_alpha = stats.norm.ppf(1 - (1 - confidence) / 2)
    z_beta = stats.norm.ppf(power)
    p = aql
    delta = aql
    n = (z_alpha * np.sqrt(p * (1 - p)) + z_beta * np.sqrt((p + delta) * (1 - (p + delta)))) ** 2 / (delta ** 2)
    return int(np.ceil(n))

def binomial_test(n, d, aql=0.1, alternative='greater'):
    test_result = stats.binomtest(d, n, p=aql, alternative=alternative)
    return test_result.pvalue

def critical_value(n, alpha, aql=0.1):
    return stats.binom.ppf(1 - alpha, n, aql)

confidence_95 = 0.95
confidence_90 = 0.90
aql = 0.1

n_95 = calculate_sample_size(confidence_95, aql)
n_90 = calculate_sample_size(confidence_90, aql)

critical_95 = critical_value(n_95, 1 - confidence_95, aql)
critical_90 = critical_value(n_90, 1 - confidence_90, aql)

print(f"95%置信水平下的样本数为: {n_95}")
print(f"90%置信水平下的样本数为: {n_90}")

print(f"95%置信水平下的临界值为: {critical_95}")
print(f"90%置信水平下的临界值为: {critical_90}")

d_95 = 19
d_90 = 14

p_val_95 = binomial_test(n_95, d_95, aql, 'greater')
p_val_90 = binomial_test(n_90, d_90, aql, 'less')

alpha_95 = 1 - confidence_95
alpha_90 = 1 - confidence_90

# 决策
if p_val_95 > alpha_95:
    print("在95%的置信水平下，无法拒绝原假设，认为次品率不超过10%，接收这批零配件。")
else:
    print("在95%的置信水平下，拒绝原假设，认为次品率超过10%，拒收这批零配件。")

if p_val_90 < alpha_90:
    print("在90%的置信水平下，无法拒绝原假设，认为次品率不超过10%，接收这批零配件。")
else:
    print("在90%的置信水平下，拒绝原假设，认为次品率超过10%，拒收这批零配件。")