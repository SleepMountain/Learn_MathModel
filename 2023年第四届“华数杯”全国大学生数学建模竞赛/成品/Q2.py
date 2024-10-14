import numpy as np
from scipy.spatial import distance


# 示例数据，实际应用中需要根据附件提供的数据进行替换
targetR = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1])
RecipeRvalues = np.random.rand(10, 16)  # 假设有10个不同的配方，每个配方有16个波长的R值

# 计算色差
def ccd(targetR, recipeR):
    return distance.euclidean(targetR, recipeR)

# 选择最优配方
def findrecipe(targetR, recipeR, number):
    bestRecipe = []
    for reciper in recipeR:
        colordifferent = ccd(targetR, reciper)
        bestRecipe.append((reciper, colordifferent))
    bestRecipe.sort(key=lambda x: x[1])  # 根据色差排序
    return bestRecipe[:number]

# 计算每个配方的色差并选择最优配方
number = 10
bestRecipes = findrecipe(targetR, RecipeRvalues, number)

# 打印最优配方和色差
for i, (recipeR, colordifferent) in enumerate(bestRecipes):
    print(f"配方{i + 1}：")
    print("R值：", recipeR)
    print("色差：", colordifferent)
    print()
