import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def objective_function(X):
    return (438 - 3 * X[0] + 0.5 * X[1]) * (0.6 / 1.6) * X[2] + \
           (626 + 2 * X[0] - 0.2 * X[2]) * (0.68 / 1.68) * X[1] + \
           (1032 + 12 * X[0] - X[1] - X[2]) * (0.86 / 1.86) * X[0]
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

x1 = np.linspace(134, 150, 100)
x2 = np.linspace(17, 18, 100)
x3 = np.linspace(13, 15, 100)
X1, X2, X3 = np.meshgrid(x1, x2, x3, indexing='ij')
Z = objective_function([X1, X2, X3])

Z[c1([X1, X2, X3]) < 0] = np.nan
Z[c2([X1, X2, X3]) < 0] = np.nan
Z[c3([X1, X2, X3]) < 0] = np.nan
Z[c4([X1, X2, X3]) < 0] = np.nan
Z[c5([X1, X2, X3]) < 0] = np.nan
Z[c6([X1, X2, X3]) < 0] = np.nan

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X1, X2, X3, c=Z, cmap='coolwarm')
ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('X3')
ax.set_title('Linear Programming Optimization')
plt.show()
