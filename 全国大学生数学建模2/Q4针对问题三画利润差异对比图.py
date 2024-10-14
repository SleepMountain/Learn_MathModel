import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False


file_path = r'D:\桌面\问题四针对问题三1.xlsx'
sheet_name = 'Sheet2'
data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

print(data.head())

sns.set(style='whitegrid')

plt.figure(figsize=(12, 8))
bars = plt.bar(data['id'], data['best profit different'],
               color=sns.color_palette('viridis', len(data)), edgecolor='black')

plt.xlabel('ID', fontsize=14)
plt.ylabel('Best Profit', fontsize=14)

plt.grid(axis='y', linestyle='--', alpha=0.7)


plt.show()