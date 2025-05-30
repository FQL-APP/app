import json
import folium
import webbrowser
from folium.plugins import HeatMap

def heatmap_plot_function(file_path: str, visualization_selection='heatmap'):
    # Initialize sums and counters
    lat_sum = 0
    lon_sum = 0
    count = 0

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Sum up all latitudes and longitudes
    for item in data['results']:
        lat = item['latitude']
        lon = item['longitude']
        if lat != 0.0 and lon != 0.0:
            lat_sum += lat
            lon_sum += lon
            count += 1

    # Calculate the average latitude and longitude (the centroid)
    if count > 0:
        center_lat = lat_sum / count
        center_lon = lon_sum / count
    else:
        center_lat, center_lon = 38, 77  # Default to Washington, D.C.

    # Create map centered on centroid
    map_obj = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    if visualization_selection == "pop up":
        for item in data['results']:
            lat = item['latitude']
            lon = item['longitude']
            id = item.get('id')
            txt = item.get('txt', 'No txt provided')
            url = f'https://www.mindat.org/loc-{id}.html'
            popup_info = folium.Popup(
                f"<div style='width:200px; font-size:16px;'><strong>ID:</strong> {id}<br>"
                f"<strong>Description:</strong> {txt}<br>"
                f"<strong>URL:</strong> <a href='{url}' target='_blank'>{url}</a></div>",
                max_width=265
            )
            if lat != 0.0 and lon != 0.0:
                folium.Marker(
                    location=[lat, lon],
                    popup=popup_info,
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(map_obj)
    elif visualization_selection == "heatmap":
        heat_map_data = [
            (item['latitude'], item['longitude']) for item in data['results']
            if item['latitude'] != 0.0 and item['longitude'] != 0.0
        ]
        HeatMap(heat_map_data).add_to(map_obj)
    else:
        raise ValueError("Please select a visualization approach!")

    # Save the map as HTML and open it in the browser
    output_file = 'output_map_Brazil.html'
    map_obj.save(output_file)
#    print(f"Map saved to {output_file}. Opening in your browser...")
    webbrowser.open(output_file)

if __name__ == "__main__":
    # 修改为你的实际 JSON 文件路径
    file_path = "mindat_locality_Brazil.json"
    # 选择 'heatmap' 或 'pop up'
    heatmap_plot_function(file_path, visualization_selection='heatmap')
