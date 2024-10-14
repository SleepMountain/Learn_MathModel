import numpy as np
import matplotlib.pyplot as plt


n = np.arange(1, 6)
y1 = 3/2 * n**2 + 7/2 * n + 2
y2 = (n + 5) * np.log2(n) + 4*n

plt.plot(n, y1, label="T1(n)")
plt.plot(n, y2, label="T2(n)")
plt.xlabel('n')
plt.legend()
plt.show()
