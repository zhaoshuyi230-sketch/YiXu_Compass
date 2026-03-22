from flask import Flask, request, send_file
import os

app = Flask(__name__)

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    # 使用绝对路径读取index.html
    index_path = os.path.join(BASE_DIR, 'index.html')
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading index.html: {str(e)}", 500

@app.route('/<path:filename>')
def serve_static(filename):
    # 处理静态文件（图片等）
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        try:
            file_path = os.path.join(BASE_DIR, filename)
            return send_file(file_path)
        except Exception as e:
            return f"Error serving file: {str(e)}", 404
    return "Not Found", 404

@app.route('/generate_report', methods=['POST'])
def generate_report():
    # 简化版：直接返回测试内容
    return "<h1>测试报告</h1><p>报告生成功能正在测试中</p>"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True, use_reloader=False)