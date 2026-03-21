from flask import Flask, request, render_template_string
import maya_kin
import os
from pyngrok import ngrok

app = Flask(__name__)

# 配置 ngrok
try:
    # 启动 ngrok 隧道，指向本地 5001 端口
    public_url = ngrok.connect(5001)
    print(f"\n--- 公网访问链接: {public_url} ---")
    print("复制以上链接发送给客户\n")
except Exception as e:
    print(f"ngrok 启动失败: {e}")
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
