from scipy import integrate
import numpy as np

def normal_distribution(x, mu, sigma):
    return np.exp(-(x - mu)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))

def calculate_area(start, end, mu, sigma):
    area, _ = integrate.quad(normal_distribution, start, end, args=(mu, sigma))
    return area

mu, sigma = 3, 1.5

area_0_to_1 = calculate_area(0, 1, mu, sigma)
area_1_to_2 = calculate_area(1, 2, mu, sigma)
area_2_to_3 = calculate_area(2, 3, mu, sigma)

total_area = area_0_to_1 + area_1_to_2 + area_2_to_3


ratio_0_to_1 = area_0_to_1 / total_area
ratio_1_to_2 = area_1_to_2 / total_area
ratio_2_to_3 = area_2_to_3 / total_area

print("0-1 区间与总面积的比: ", ratio_0_to_1)
print("1-2 区间与总面积的比: ", ratio_1_to_2)
print("2-3 区间与总面积的比: ", ratio_2_to_3)
