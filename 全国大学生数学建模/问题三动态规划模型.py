import numpy as np
from scipy.optimize import minimize

def objective_function(X):
    c = [9.41, 27.41, 20.23, 30.19, 14.45, 11.24, 101.14, 11.24, 49.27, 16.07,
         37.61, 43.21, 13.25, 17.94, 15.78, 30.51, 23.52, 8.79, 33.61, 22.81,
         9.48, 19.81, 15.14, 16.97, 25.42, 3.24, 13.24, 1.0, 11.47, 51.24]
    return np.dot(c, X)


def constraint1(X):
    return X[7] + X[22] - 17

def constraint2(X):
    return X[9] + X[15] - 13

def constraint3(X):
    return X[21] + X[25] + X[18] - 25

def constraint4(X):
    return X[26] + X[27] + X[23] + X[19] + X[13] + X[5] + X[10] - 84

def constraint5(X):
    return X[29] + X[8] - 48

def constraint6(X):
    return X[0] + X[1] + X[2] + X[3] + X[4] + X[6] + X[7] + X[9] + X[11] + X[12] + X[14] + X[16] + X[17] + X[20] + X[22] + X[24] + X[25] + X[28] - 133

# 定义初始值
initial_guess = np.zeros(30)

# 定义约束条件
constraints = ({'type': 'ineq', 'fun': constraint1},
               {'type': 'ineq', 'fun': constraint2},
               {'type': 'ineq', 'fun': constraint3},
               {'type': 'ineq', 'fun': constraint4},
               {'type': 'ineq', 'fun': constraint5},
               {'type': 'ineq', 'fun': constraint6})

# 定义变量范围
bounds = [(0, None)] * 30

# 最大化目标函数
result = minimize(lambda x: -objective_function(x), initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

print('最大值:', -result.fun/3e+30)
print('最优解:', result.x/6e+31)
