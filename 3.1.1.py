import os
import json
import networkx as nx
from pyvis.network import Network
import math
import webbrowser

# 定义颜色映射
color_map = {
    1: 'red',
    2: 'orange',
    3: 'goldenrod',
    4: 'green',
    5: 'blue',
    6: 'indigo',
    7: 'violet',
    8: 'purple',
    9: 'brown',
    10: 'grey',
    11: 'black'
}

# 定义Strunz分类图例
legend_html = """
<div style="position: absolute; bottom: 50px; left: 10px; background-color: white; padding: 10px; border: 1px solid black; z-index: 9999;">
    <b>Strunz分类</b><br>
    1. <span style="color: red;">元素</span><br>
    2. <span style="color: orange;">硫化物和磺化盐</span><br>
    3. <span style="color: goldenrod;">卤化物</span><br>
    4. <span style="color: green;">氧化物</span><br>
    5. <span style="color: blue;">碳酸盐</span><br>
    6. <span style="color: indigo;">硼酸盐</span><br>
    7. <span style="color: violet;">硫酸盐</span><br>
    8. <span style="color: purple;">磷酸盐、砷酸盐、钒酸盐</span><br>
    9. <span style="color: brown;">硅酸盐</span><br>
    10. <span style="color: grey;">有机化合物</span><br>
    11. <span style="color: black;">其他</span><br>
</div>
"""

# 加载并绘制矿物网络图
def network_plot_function(file_path: str, top_n=50):
    # 加载JSON数据
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 选择前n个矿物数据
    filtered_data = data["results"][:top_n]

    # 创建一个图对象
    G = nx.Graph()

    # 用于保存矿物和产地的映射
    mineral_locality_map = {}

    # 添加矿物节点
    for mineral in filtered_data:
        mineral_id = mineral["id"]
        mineral_name = mineral["name"]
        localities = mineral["locality"]
        strunz_value = mineral.get("strunz10ed1", 11)  # 默认值为11

        # 确保strunz_value是有效的整数
        try:
            strunz_value = int(strunz_value)
        except (ValueError, TypeError):
            strunz_value = 11  # 默认值为11

        color = color_map.get(strunz_value, 'black')  # 默认颜色为黑色

        # 根据产地数量计算节点大小
        node_size = 20 + math.log1p(len(localities)) * 10

        # 添加矿物节点，大小根据产地数量调整，颜色根据strunz10ed1值调整
        G.add_node(mineral_id, label=mineral_name, color=color, size=node_size, font_size=20)

        for locality in localities:
            if locality not in mineral_locality_map:
                mineral_locality_map[locality] = set()
            mineral_locality_map[locality].add(mineral_id)

    # 为共享同一产地的矿物添加边
    for locality, minerals in mineral_locality_map.items():
        minerals = list(minerals)
        for i in range(len(minerals)):
            for j in range(i + 1, len(minerals)):
                G.add_edge(minerals[i], minerals[j], color='grey')

    # 创建PyVis网络图
    net = Network(notebook=True, height="100vh", width="100%", cdn_resources='in_line')

    # 设置布局为圆形
    net.repulsion(node_distance=400, central_gravity=0.1, spring_length=200, spring_strength=0.05, damping=0.09)

    # 将networkx图添加到PyVis网络
    net.from_nx(G)

    # 定制节点和标签的大小
    for node in net.nodes:
        node["font"] = {"size": node.get("size", 20)}

    # 保存网络图到HTML文件，指定utf-8编码
    output_file_path = "minerals_network.html"
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(net.generate_html())

    # 插入图例到HTML内容中
    with open(output_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 找到插入点
    insertion_point = html_content.find('<body>') + len('<body>')
    html_content_with_legend = html_content[:insertion_point] + legend_html + html_content[insertion_point:]

    # 将合成后的HTML内容写入文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content_with_legend)

    # 在浏览器中打开HTML文件
    webbrowser.open(output_file_path)

    return "Successfully plotted the required diagram with legend."

# 使用示例
file_path = "geomaterials_矿物共生与网络分析.json"
network_plot_function(file_path)
