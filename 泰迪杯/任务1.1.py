import pandas as pd

def calculate_percentage(filename, sheetname, fieldname, target_value):
    # 读取Excel表格
    df = pd.read_excel(filename, sheet_name=sheetname)


    # 筛选特定字段
    field = df[fieldname]

    # 计算特定值出现的次数
    count = field[field == target_value].count()

    # 计算占比
    percentage = count / len(field)

    return percentage

# 测试
filename = "D:/比赛/准备/泰迪杯/A题-档案数字化加工流程数据分析/result3.xlsx"
sheetname = "Sheet1"
fieldname = "iNODE_STATUS"
target_value = 5

percentage = calculate_percentage(filename, sheetname, fieldname, target_value)
print("该数字数据在字段中出现的次数占比为: {:.2%}".format(percentage))