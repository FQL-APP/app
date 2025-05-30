import pandas as pd
import tkinter as tk
from tkinter import messagebox

# 读取CSV文件并确保年份是数字格式
def load_data(file_path):
    data = pd.read_csv(file_path)



    return data

# 根据 id 或 name 查找矿物
def find_mineral_by_id_or_name(data, search_value):
    # 检查输入值是数字（id）还是字符串（name）
    if search_value.isdigit():
        # 搜索 id
        result = data[data['id'] == int(search_value)]
    else:
        # 搜索 name（部分匹配）
        result = data[data['name'].str.contains(search_value, case=False, na=False)]

    return result

# 显示查询结果
def show_results():
    # 获取用户输入
    search_value = entry_search.get()

    # 加载数据
    data = load_data('entrytype.csv')  # 请确保CSV路径正确

    # 查找矿物
    result = find_mineral_by_id_or_name(data, search_value)

    # 显示结果
    if not result.empty:
        result_text = "矿物记录:\n"
        for _, row in result.iterrows():
            result_text += f"ID: {row['id']}\n"
            result_text += f"矿物名称(Name): {row['name']}\n"
            result_text += f"元素(Elements): {row['elements']}\n"
            result_text += f"硬度最小值(Hardness Min): {row['hmin']}\n"
            result_text += f"硬度最大值(Hardness Max): {row['hmax']}\n"
            result_text += f"密度最小值(Density Min): {row['dmeas']}\n"
            result_text += f"密度最大值(Density Max): {row['dmeas2']}\n"
            result_text += f"颜色(Colour): {row['colour']}\n"
            result_text += f"晶体结构(Crystal System): {row['csystem']}\n"
            result_text += f"发现年份(Discovery Year): {row['discovery_year']}\n"
            result_text += "-" * 40 + "\n"
        label_result.config(text=result_text)
    else:
        label_result.config(text="No mineral found with the given ID or Name.")

# 创建主窗口
root = tk.Tk()
root.title("矿物属性查询系统")

# 设置字体为 Times New Roman
font_style = ('Times New Roman', 12)

# 创建输入字段
label_search = tk.Label(root, text="输入矿物ID或名称(Name):", font=font_style)
label_search.grid(row=0, column=0)
entry_search = tk.Entry(root, font=font_style)
entry_search.grid(row=0, column=1)

# 显示查询结果
label_result = tk.Label(root, text="", justify="left", font=font_style)
label_result.grid(row=2, column=0, columnspan=2)

# 查询按钮
btn_search = tk.Button(root, text="查询", command=show_results, font=font_style)
btn_search.grid(row=1, column=0, columnspan=2)

# 启动主循环
root.mainloop()
