import numpy as np
from scipy.optimize import curve_fit

def cubic_fit(x, a, b, c, d, e, f, g, h, i):
    x1, x2 = x
    return a*x1**3 + b*x1**2 + c*x1 + d*x2**3 + e*x2**2 + f*x2 + g*x1*x2**2 + h*x1*x2 + i

def quadratic_fit(x, a, b, c, d, e, f, g, h):
    x1, x2 = x
    return a*x1**2 + b*x1 + c*x2**2 + d*x2 + e*x1*x2 + f*x1 + g*x2 + h


data = [
    (0.000, 1529.808, 2.219489863),
    (0.600, 1529.807, 2.216742969),
    (1.200, 1529.813, 2.23322433),
    (1.800, 1529.812, 2.230477436),
    (2.400, 1529.814, 2.235971223),
    (3.000, 1529.809, 2.222236756),
    (0.000, 1540.095, 0.259090909),
    (0.600, 1541.092, 2.978181818),
    (1.200, 1542.090, 5.7),
    (1.800, 1543.093, 8.435454545),
    (2.400, 1544.094, 11.16545455),
    (3.000, 1545.091, 13.88454545)
]

X = np.array([(x1, x2) for x1, x2, _ in data])
y = np.array([y for _, _, y in data])

popt_cubic, pcov_cubic = curve_fit(cubic_fit, X, y)
print("Cubic Fit Parameters:", popt_cubic)

popt_quadratic, pcov_quadratic = curve_fit(quadratic_fit, X, y)
print("Quadratic Fit Parameters:", popt_quadratic)