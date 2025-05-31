import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

# 路由：运行指定的 Python 脚本并生成 HTML 文件
@app.route("/run", methods=["GET"])
def run_code():
    script_name = request.args.get("script", "3.1.3.py")  # 默认运行 3.1.3.py
    try:
        # 执行指定脚本，生成 HTML 文件
        result = subprocess.check_output(["python3", script_name], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = f"错误：\n{e.output}"
    except Exception as e:
        result = str(e)
    return jsonify({"output": result})

# 路由：获取 geomaterials.json 数据
@app.route('/geomaterials', methods=["GET"])
def get_geomaterials():
    try:
        # 确保读取当前目录下的 geomaterials.json
        file_path = os.path.join(os.path.dirname(__file__), 'geomaterials.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 路由：返回 minerals_network.html 文件
@app.route('/minerals_network.html', methods=["GET"])
def get_html_file():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'minerals_network.html')
        return send_from_directory(os.path.dirname(__file__), 'minerals_network.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output_map_Brazil.html', methods=["GET"])
def get_html1_file():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'output_map_Brazil.html')
        return send_from_directory(os.path.dirname(__file__), 'output_map_Brazil.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/minerals_elements_network.html', methods=["GET"])
def get_html2_file():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'minerals_elements_network.html')
        return send_from_directory(os.path.dirname(__file__), 'minerals_elements_network.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 可选：暴露任意文件，推荐只在测试用
# @app.route('/file/<path:filename>')
# def serve_file(filename):
#     dir_path = os.path.dirname(os.path.abspath(__file__))
#     return send_from_directory(dir_path, filename)

if __name__ == "__main__":
    # 启动 Flask 服务，监听 0.0.0.0 地址，端口 80
    app.run(host="0.0.0.0", port=80)
