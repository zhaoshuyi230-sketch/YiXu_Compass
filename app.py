from flask import Flask, request, send_file, Response, stream_with_context
import maya_kin
import os
import json

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
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    
    if not all([year, month, day]):
        return "请选择完整的日期"
    
    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # 调用 build_report 函数生成报告并直接返回 HTML 内容
    html_content = maya_kin.build_report(date_str)
    return Response(html_content, mimetype='text/html')

@app.route('/stream_report', methods=['POST'])
def stream_report():
    """流式生成报告"""
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    
    if not all([year, month, day]):
        return "请选择完整的日期", 400
    
    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    def generate():
        try:
            # 获取玛雅印记信息
            kin_info = maya_kin.get_kin_by_date(*map(int, date_str.split('-')))
            kin_name = kin_info['name']
            kin_number = kin_info.get('kin', 0)
            
            # 发送开始信号
            yield f"data: {json.dumps({'type': 'start', 'kin_name': kin_name, 'kin_number': kin_number})}\n\n"
            
            # 获取流式响应
            response = maya_kin.generate_report(kin_name)
            
            # 处理流式响应
            full_content = ""
            if hasattr(response, '__iter__') and not isinstance(response, str):
                for chunk in response:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            full_content += delta.content
                            yield f"data: {json.dumps({'type': 'content', 'content': delta.content})}\n\n"
                
                # 发送完成信号
                yield f"data: {json.dumps({'type': 'complete', 'content': full_content})}\n\n"
            else:
                # 非流式响应（错误情况）
                yield f"data: {json.dumps({'type': 'complete', 'content': str(response)})}\n\n"
                
        except Exception as e:
            print(f"Stream error: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True, use_reloader=False)
