import pandas as pd
import os

# Define file paths
excel_file_path = r'D:\桌面\诗人数据集.xlsx'
sheet_name = '诗人表'
json_file_path = r'D:\桌面\1\诗人表.json'


# Read the Excel file
df = pd.read_excel(excel_file_path, sheet_name=sheet_name, engine='openpyxl')

# Ensure the output directory exists
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

# Convert the DataFrame to JSON and save it
df.to_json(json_file_path, orient='records', force_ascii=False, indent=4)