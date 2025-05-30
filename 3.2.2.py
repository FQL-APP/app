import json
from collections import defaultdict

# 读取 geomaterials.json 文件
file_path = 'geomaterials.json'  # 请替换为实际文件路径
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 目标矿物名称，假设为 'Acanthite'
target_mineral = 'Acanthite'  # 请替换为实际目标矿物名称

# 找到目标矿物的 locality 列表
target_mineral_record = None
for record in data['results']:
    if record['name'] == target_mineral:
        target_mineral_record = record
        break

# 如果找不到目标矿物，输出并退出
if not target_mineral_record:
    print(f"找不到矿物名称为 {target_mineral} 的记录")
    exit()

target_localities = set(target_mineral_record.get('locality', []))

# 输出目标矿物的 locality 数量
#print(f"目标矿物 '{target_mineral}' 的 locality 数量: {len(target_localities)}")

# 用来存储矿物与指定矿物共享 locality 数量的字典
minerals_match_count = defaultdict(int)

# 遍历所有矿物记录，统计与目标矿物相同 locality 的矿物
for record in data['results']:
    if record['name'] == target_mineral:
        continue  # 跳过目标矿物本身

    current_localities = set(record.get('locality', []))
    # 找到与目标矿物共享 locality 的数量
    common_localities = target_localities & current_localities
    if common_localities:
        minerals_match_count[record['name']] += len(common_localities)

# 按照匹配数量排序，找出与目标矿物匹配最多的矿物记录
sorted_minerals = sorted(minerals_match_count.items(), key=lambda x: x[1], reverse=True)

# 输出匹配最多的前10个矿物（按频率降序排列）
if sorted_minerals:
    print(f"\n{target_mineral} 共生关系排序(按频率排序)")
    print("=" * 45)  # 输出分隔线

    # 按频率降序排序（频率高的在前）
    sorted_by_frequency = sorted(sorted_minerals, key=lambda x: x[1], reverse=True)

    # 只取前10个
    top_10_minerals = sorted_by_frequency[:10]

    # 计算最长矿物名称的长度，用于动态对齐
    max_name_length = max(len(mineral) for mineral, _ in top_10_minerals)

    # 格式化输出
    for idx, (mineral, count) in enumerate(top_10_minerals, 1):
        # 使用动态宽度对齐，确保列对齐
        print(f"{idx:>2}. 矿物: {mineral:<{max_name_length}}  频率: {count:>5}")
else:
    print(f"\n没有找到与目标矿物 '{target_mineral}' 共享 locality 的矿物")