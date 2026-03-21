from flask import Flask, request
import maya_kin
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 直接返回index.html
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
    
    # 调用 build_report 函数生成报告并直接返回 HTML 内容
    html_content = maya_kin.build_report(date_str)
    from flask import Response
    return Response(html_content, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True, use_reloader=False)
