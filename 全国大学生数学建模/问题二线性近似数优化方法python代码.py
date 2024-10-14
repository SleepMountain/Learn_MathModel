import numpy as np
from scipy.optimize import minimize


def obfunction(X):
    return (453 + 5 * X[0] - 0.2 * X[1] - 0.1 * X[0]) * (0.86 / 1.86) * X[5] + \
           (626 + 7.5 * X[0] - 0.5 * X[1]) * (0.68 / 1.68) * X[4] + \
           (326 + 4 * X[0] - 0.5 * X[1]) * (0.51 / 1.51) * X[3] + \
           (438 - 3 * X[0] + 0.5 * X[1]) * (0.6 / 1.6) * X[2] + \
           (626 + 2 * X[0] - 0.2 * X[3]) * (0.68 / 1.68) * X[1] + \
           (1032 + 12 * X[0] - X[1] - X[3]) * (0.86 / 1.86) * X[0]

def c1(X):
    return X[0] - 134

def c2(X):
    return 150 - X[0]

def c3(X):
    return X[1] - 17

def c4(X):
    return 18 - X[1]

def c5(X):
    return X[2] - 13

def c6(X):
    return 15 - X[2]

def c7(X):
    return X[3] - 25

def c8(X):
    return 27 - X[3]

def c9(X):
    return X[4] - 84

def c10(X):
    return 90 - X[4]

def c11(X):
    return X[5] - 48

def c12(X):
    return 50 - X[5]

ig = np.array([135, 17.5, 13.5, 25.5, 84.5, 48.5])

constraints = ({'type': 'ineq', 'fun': c1},
               {'type': 'ineq', 'fun': c2},
               {'type': 'ineq', 'fun': c3},
               {'type': 'ineq', 'fun': c4},
               {'type': 'ineq', 'fun': c5},
               {'type': 'ineq', 'fun': c6},
               {'type': 'ineq', 'fun': c7},
               {'type': 'ineq', 'fun': c8},
               {'type': 'ineq', 'fun': c9},
               {'type': 'ineq', 'fun': c10},
               {'type': 'ineq', 'fun': c11},
               {'type': 'ineq', 'fun': c12})

result = minimize(obfunction, ig, method='SLSQP', constraints=constraints)

print('最大值:', result.fun)
print('最优解:', result.x)
