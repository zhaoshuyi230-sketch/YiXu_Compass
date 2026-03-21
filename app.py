from flask import Flask, request, render_template_string
import maya_kin
import os


app = Flask(__name__)

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML_PATH = os.path.join(BASE_DIR, 'index.html')

try:
    # 检查 index.html 是否存在
    if not os.path.exists(INDEX_HTML_PATH):
        print(f"警告: 找不到 {INDEX_HTML_PATH}")
        print("请确保 index.html 确实在项目根目录下\n")
    
    
    print(f"\n--- 公网访问链接: {public_url} ---")
    print("复制以上链接发送给客户\n")
except Exception as e:
    
    print("请确保网络连接正常\n")

@app.route('/')
def index():
    # 使用绝对路径读取 index.html
    if not os.path.exists(INDEX_HTML_PATH):
        return f"错误: 找不到 index.html 文件，请确保文件存在于: {BASE_DIR}", 500
    
    with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()

try:
    
    
    print(f"\n--- 公网访问链接: {public_url} ---")
    print("复制以上链接发送给客户\n")
except Exception as e:
    
    print("请确保网络连接正常\n")

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/generate_report', methods=['POST'])
def generate_report():
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    
    if not all([year, month, day]):
        return "请选择完整的日期"
    
    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # 调用 build_report 函数生成报告
    maya_kin.build_report(date_str)
    
    # 计算 kin 编号以获取生成的文件名
    details = maya_kin.get_kin_details(date_str)
    kin_number = details.get('kin', 0)
    file_name = f"KIN_{kin_number}_BlackGold_Report.html"
    
    # 读取生成的 HTML 文件并返回内容
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "报告生成失败，请重试"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002, threaded=True, use_reloader=False)
