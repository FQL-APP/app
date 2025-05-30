import json
import networkx as nx
from pyvis.network import Network
import math
from collections import Counter

def network_plot_function(file_path: str, top_n=100):
    # Define a color map for strunz10ed1 values
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

    # Define a legend for the Strunz classification
    legend_html = """
<div style="position: absolute; bottom: 50px; left: 10px; background-color: white; padding: 10px; border: 1px solid black; z-index: 9999; font-family: 'Times New Roman', serif;">
    <b>矿物节点-Strunz分类</b><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: red; border-radius: 50%; margin-right: 5px;"></span><span style="color: red;">元素(1)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: orange; border-radius: 50%; margin-right: 5px;"></span><span style="color: orange;">硫化物和磺化盐(2)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: goldenrod; border-radius: 50%; margin-right: 5px;"></span><span style="color: goldenrod;">卤化物(3)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: green; border-radius: 50%; margin-right: 5px;"></span><span style="color: green;">氧化物(4)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: blue; border-radius: 50%; margin-right: 5px;"></span><span style="color: blue;">碳酸盐(5)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: indigo; border-radius: 50%; margin-right: 5px;"></span><span style="color: indigo;">硼酸盐(6)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: violet; border-radius: 50%; margin-right: 5px;"></span><span style="color: violet;">硫酸盐(7)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: purple; border-radius: 50%; margin-right: 5px;"></span><span style="color: purple;">磷酸盐、砷酸盐、钒酸盐(8)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: brown; border-radius: 50%; margin-right: 5px;"></span><span style="color: brown;">硅酸盐(9)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: grey; border-radius: 50%; margin-right: 5px;"></span><span style="color: grey;">有机化合物(10)</span><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: black; border-radius: 50%; margin-right: 5px;"></span><span style="color: black;">其他(11)</span><br>
    <b>元素节点</b><br>
    <span style="display: inline-block; width: 15px; height: 15px; background-color: pink; border-radius: 50%; margin-right: 5px;"></span><span style="color: pink;">化学元素</span><br>
</div>
"""
    # Load the JSON data from the file
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)

    # Filter data to include only the top n minerals
    filtered_data = data["results"][:top_n]

    # Create a graph
    G = nx.Graph()

    # Initialize a counter to track element frequencies
    element_counter = Counter()

    # Extract and add nodes to the graph
    mineral_locality_map = {}
    for mineral in filtered_data:
        mineral_id = mineral["id"]
        mineral_name = mineral["name"]
        localities = mineral["locality"]
        strunz_value = mineral.get("strunz10ed1", 11)  # Default to 11 if not present

        # Ensure strunz_value is a valid integer
        try:
            strunz_value = int(strunz_value)
        except (ValueError, TypeError):
            strunz_value = 11  # Default to 11 if conversion fails

        color = color_map.get(int(strunz_value), 'black')  # Default to black if out of range

        # Calculate node size using logarithm of the number of localities
        node_size = 20 + math.log1p(len(localities)) * 10  # Adjust the scaling factor as needed

        # Add a node for the mineral with size proportional to the number of localities and colored by strunz10ed1 value
        G.add_node(mineral_id, label=mineral_name, color=color, size=node_size, font_size=20)

        # Add element nodes and edges
        elements = mineral.get("elements", [])
        for element in elements:
            # Count the frequency of each element
            element_counter[element] += 1

            # Add element node if not already in the graph
            if element not in G:
                G.add_node(element, label=element, color='pink')

            # Add an edge between the mineral and the element
            G.add_edge(mineral_id, element, color='grey')

        # Add edges between minerals that share at least one locality
        for locality in localities:
            if locality not in mineral_locality_map:
                mineral_locality_map[locality] = set()
            mineral_locality_map[locality].add(mineral_id)

    # Add edges between minerals that share at least one locality
    # for locality, minerals in mineral_locality_map.items():
    #     minerals = list(minerals)
    #     for i in range(len(minerals)):
    #         for j in range(i + 1, len(minerals)):
    #             G.add_edge(minerals[i], minerals[j], color='grey')

    # Calculate element node size based on frequency
    max_element_count = max(element_counter.values(), default=1)
    for element in G.nodes:
        if element not in filtered_data:  # Only resize element nodes
            element_size = 20 + (element_counter[element] / max_element_count) * 50  # Adjust size scaling
            G.nodes[element]['size'] = element_size

    # Create a PyVis network
    net = Network(notebook=True, height="100vh", width="100%", cdn_resources='in_line')

    # Set the layout to circular
    net.repulsion(node_distance=100, central_gravity=0.1, spring_length=100, spring_strength=0.05, damping=0.09)

    # Add the graph to the PyVis network
    net.from_nx(G)

    # Customize node and label sizes
    for node in net.nodes:
        node["font"] = {"size": node.get("size", 40)}

    # Save the network to an HTML file with UTF-8 encoding
    output_file_path = "minerals_elements_network.html"
    try:
        net.save_graph(output_file_path)
    except UnicodeEncodeError:
        # If default save fails, try with explicit UTF-8 encoding
        html = net.generate_html()
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html)

    # Insert the legend into the network HTML content with UTF-8 encoding
    with open(output_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find the insertion point for the legend
    insertion_point = html_content.find('<body>') + len('<body>')
    html_content_with_legend = html_content[:insertion_point] + legend_html + html_content[insertion_point:]

    # Write the combined HTML to the file with UTF-8 encoding
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content_with_legend)

#    print(f"Network visualization saved to {output_file_path}")
    return "Successfully plotted the required diagram with legend and elements."

# Example usage:
if __name__ == "__main__":
    # Set your file path here
    file_path = "geomaterials_矿物-元素网络分析.json"

    # Call the function
    result = network_plot_function(file_path)
#    print(result)