import numpy as np
from scipy.optimize import curve_fit

def cubic_fit(x, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x0, y, z):
    x1, x2 = x
    return a*x1**3 + b*x1**2 + c*x1 + d*x2**3 + e*x2**2 + f*x2 + g*x1*x2**2 + h*x1*x2 + i*x1**2*x2 + j*x1**2 + k*x1*x2 + l*x1 + m*x2**2 + n*x2 + o*x1*x2**2 + p*x1*x2 + q*x1 + r*x2**2 + s*x2 + t*x1*x2 + u*x1 + v*x2 + w*x1**2 + x0*x1 + y*x2**2 + z*x2

def quadratic_fit(x, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x0, y, z):
    x1, x2 = x
    return a*x1**2 + b*x1 + c*x2**2 + d*x2 + e*x1*x2 + f*x1 + g*x2 + h*x1**2 + i*x1 + j*x2**2 + k*x2 + l*x1*x2 + m*x1 + n*x2 + o*x1**2 + p*x1 + q*x2**2 + r*x2 + s*x1*x2 + t*x1 + u*x2 + v*x1**2 + w*x1 + x0*x2**2 + y*x2 + z


# 数据
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