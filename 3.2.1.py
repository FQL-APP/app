# 1

import json

# 读取 JSON 文件
file_path = 'geomaterials.json'  # 请替换为实际文件路径
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 目标 locality 值
target_locality = 142692  # 请替换为您要筛选的 locality 值

# 筛选出 locality 属性中包含 target_locality 的记录
filtered_records = [item for item in data['results'] if target_locality in item.get('locality', [])]

# 输出筛选结果
#print(f"共找到 {len(filtered_records)} 条 locality 中包含 {target_locality} 的记录:")
#print("=" * 40)  # 输出一条分隔线
#for record in filtered_records:
#    print(f"矿物名称: {record['name']}, ID: {record['id']}")

# 将筛选后的记录保存到新文件
output_file_path = 'filtered_geomaterials.json'  # 新文件路径
with open(output_file_path, 'w', encoding='utf-8') as f_out:
    json.dump({"results": filtered_records}, f_out, ensure_ascii=False, indent=4)

# print(f"筛选后的记录已保存为 {output_file_path}")


# 2

import json
from collections import defaultdict

# 读取 JSON 文件
file_path = 'filtered_geomaterials.json'  # 请替换为实际文件路径
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 用字典收集 locality 和对应的矿物名称
locality_dict = defaultdict(list)

# 遍历记录，将 locality 作为键，矿物名称作为值，存入 locality_dict
for record in data['results']:
    for locality in record.get('locality', []):
        locality_dict[locality].append(record['name'])

# 筛选出在同一个 locality 中，至少有 4 个矿物名称的 locality 值
valid_localities = {locality: names for locality, names in locality_dict.items() if len(names) >= 4}

# 排除 target_locality
target_locality = 142692
if target_locality in valid_localities:
    del valid_localities[target_locality]

# 将符合条件的 locality 和矿物名称组合保存到新的文件中
output_data = []

for locality, names in valid_localities.items():
    locality_record = {
        'locality': locality,
        'minerals': names
    }
    output_data.append(locality_record)

# 保存到新的文件
output_file_path = 'filtered_localities.json'  # 新文件路径
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump({'valid_localities': output_data}, f, ensure_ascii=False, indent=4)

# print(f"共找到 {len(valid_localities)} 个 locality，每个 locality 至少包含 4 个矿物名称组合，已保存至 {output_file_path}")


# 3

import json
# 读取 filtered_localities.json 文件
with open('filtered_localities.json', 'r', encoding='utf-8') as f:
    filtered_localities = json.load(f)

# 提取 filtered_localities.json 中的 locality 值集合
localities_to_check = {loc['locality'] for loc in filtered_localities['valid_localities']}

# 读取 geomaterials.json 文件
with open('geomaterials.json', 'r', encoding='utf-8') as f:
    geomaterials = json.load(f)

# 排除 locality 为 142692 的记录
exclude_locality = 142692

# 用来保存矿物名称、匹配频率和匹配的 locality 列表的字典
minerals_info = {}

# 遍历 geomaterials.json 中的每条记录，检查其 locality 值
for record in geomaterials['results']:
    # 检查该记录是否包含 locality 142692，如果有则跳过
    if exclude_locality in record['locality']:
        continue  # 排除当前记录

    # 获取当前记录的 locality 列表
    current_localities = record['locality']

    # 计算该记录中有多少个 locality 与 filtered_localities.json 中的 locality 匹配
    matching_localities = [loc for loc in current_localities if loc in localities_to_check]

    # 如果有匹配的 locality，则增加其匹配频率并记录匹配的 locality
    if matching_localities:
        mineral_name = record['name']
        if mineral_name not in minerals_info:
            minerals_info[mineral_name] = {'frequency': 0, 'localities': []}
        minerals_info[mineral_name]['frequency'] += len(matching_localities)
        minerals_info[mineral_name]['localities'].extend(matching_localities)

# 排序并选择频率前二十的记录
sorted_minerals = sorted(minerals_info.items(), key=lambda x: x[1]['frequency'], reverse=True)[:20]
print()  # 输出一个空行
# 输出前二十个矿物名称及其匹配频率（按频率降序排列）
print("前二十个矿物名称及其匹配频率(按频率排序)")
print("=" * 40)  # 输出一条分隔线

# 按频率降序排序（频率高的在前）
sorted_by_frequency = sorted(sorted_minerals, key=lambda x: x[1]['frequency'], reverse=True)

# 只取前20个
top_20_minerals = sorted_by_frequency[:20]

# 计算最长矿物名称的长度，用于动态对齐
max_name_length = max(len(mineral) for mineral, _ in top_20_minerals)

# 格式化输出
for idx, (mineral, info) in enumerate(top_20_minerals, 1):
    # 使用动态宽度对齐，确保列对齐
    print(f"{idx:>2}. 矿物: {mineral:<{max_name_length}}  频率: {info['frequency']:>5}")



















