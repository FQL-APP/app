import sys
import pandas as pd

# 假设这行代码是用来加载矿物数据的
# 请根据实际情况修改路径或数据加载方式
data = pd.read_csv('entrytype.csv')

# 获取查询参数
def get_query_params():
    query_params = {
        "elements": sys.argv[1] if len(sys.argv) > 1 else "",
        "hardness": sys.argv[2] if len(sys.argv) > 2 else "",
        "density": sys.argv[3] if len(sys.argv) > 3 else "",
        "colour": sys.argv[4] if len(sys.argv) > 4 else "",
        "csystem": sys.argv[5] if len(sys.argv) > 5 else "",
        "year": sys.argv[6] if len(sys.argv) > 6 else "",
    }
    return query_params

# 筛选数据的函数
def filter_data(data, elements, hardness, density, colour, csystem, year):
    if elements:
        data = data[data['元素组成'].str.contains(elements, case=False)]
    if hardness:
        data = data[data['硬度'] == float(hardness)]
    if density:
        data = data[data['密度'] == float(density)]
    if colour:
        data = data[data['颜色'].str.contains(colour, case=False)]
    if csystem:
        data = data[data['晶体结构'].str.contains(csystem, case=False)]
    if year:
        data = data[data['发现年份'] == int(year)]
    return data

# 获取查询条件
params = get_query_params()

# 根据查询条件筛选数据
filtered_data = filter_data(data, params["elements"], params["hardness"], params["density"], params["colour"], params["csystem"], params["year"])

# 输出筛选后的结果
if not filtered_data.empty:
    result = ""
    for index, row in filtered_data.iterrows():
        result += f"ID: {row['id']}, 名称: {row['name']}\n"
else:
    result = "没有找到符合条件的矿物"

# 输出结果
print(result)
