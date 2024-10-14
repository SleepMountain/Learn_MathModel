import os
import pandas as pd

file_path =r'D:\桌面\data.xlsx'
if os.path.exists(file_path):
    print("文件存在")
else:
    print("文件不存在")


data = pd.read_excel(file_path)
print(data.columns)

