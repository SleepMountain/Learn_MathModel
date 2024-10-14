import numpy as np


def func(x):
    return 1 - (0.45*np.pi*0.1/8*x**3 - 0.45*np.pi*5.275*0.1/8*x**2 + (0.45*np.pi*3.57675*0.1+1.14*8)/8*x - 0.3249 - 0.45*np.pi*0.1/8*0.3249)/(x**2)

x = np.array([3, 6, 9, 12, 15, 18, 21, 24])
y_actual = np.array([0.6556, 0.8124, 0.8301, 0.7842, 0.7612, 0.7042, 0.6586, 0.6075])

y_predicted = func(x)
errors = y_actual - y_predicted
rmse = np.sqrt(np.mean(errors**2))

print("RMSE:", rmse)

