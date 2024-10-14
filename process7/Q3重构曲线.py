import numpy as np
import matplotlib.pyplot as plt


curvatures_test1 = [0.000192, 0.000192, 0.000194, 0.000193, 0.000194, 0.000193]
curvatures_test2 = [0.000261, 0.000260, 0.000498, 0.000736, 0.000975, 0.001212]


x_coords = np.arange(0, 3.1, 0.6)


theta_initial = np.pi / 4



x_plot_test1, y_plot_test1 = [], []
x_plot_test2, y_plot_test2 = [], []



def plot_curve(x_coords, curvatures, color, label):
    x, y = 0, 0
    theta = theta_initial
    x_plot, y_plot = [], []
    x_plot.append(x), y_plot.append(y)

    for i in range(len(x_coords) - 1):

        curvature = np.mean([curvatures[i], curvatures[i + 1]])
        dx = x_coords[i + 1] - x_coords[i]

        dtheta = curvature * dx

        theta += dtheta

        for _ in np.linspace(0, 1, int(dx * 10) + 1):
            x_end = x + _ * dx * np.cos(theta)
            y_end = y + _ * dx * np.sin(theta)
            x_plot.append(x_end)
            y_plot.append(y_end)

        x, y = x_end, y_end


    x_plot.append(x_coords[-1]), y_plot.append(y)


    plt.plot(x_plot, y_plot, color=color, label=label)



plot_curve(x_coords, curvatures_test1, 'blue', 'Approximate Curve Test 1')

plot_curve(x_coords, curvatures_test2, 'red', 'Approximate Curve Test 2')

plt.xlabel('x (meters)')
plt.ylabel('y (meters)')
plt.title('Approximate Plane Curve Reconstruction Based on Curvature Data')
plt.grid(True)
plt.legend()
plt.show()