from flask import Flask, request
import maya_kin
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 使用绝对路径读取 index.html，确保在任何环境中都能找到
    current_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(current_dir, 'index.html')
    
    if not os.path.exists(index_path):
        # 如果找不到文件，返回一个简单的 HTML 页面
        return '''
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>财富天赋罗盘</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
                    background-color: #1a1a1a;
                    color: #d4af37;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                .container {
                    width: 100%;
                    max-width: 600px;
                    padding: 40px;
                    background-color: rgba(20, 20, 20, 0.8);
                    border: 1px solid #d4af37;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                }
                h1 {
                    text-align: center;
                    font-size: 2.8em;
                    margin-bottom: 40px;
                    color: #d4af37;
                    text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
                    letter-spacing: 3px;
                }
                .date-selector {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 40px;
                    gap: 20px;
                }
                .select-group {
                    flex: 1;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                    color: #d4af37;
                }
                select {
                    width: 100%;
                    padding: 15px;
                    background-color: #2a2a2a;
                    border: 1px solid #d4af37;
                    border-radius: 8px;
                    color: #d4af37;
                    font-size: 16px;
                    cursor: pointer;
                }
                .submit-button {
                    width: 100%;
                    padding: 20px;
                    background: linear-gradient(135deg, #d4af37 0%, #a67c00 100%);
                    border: none;
                    border-radius: 10px;
                    color: #1a1a1a;
                    font-size: 1.4em;
                    font-weight: bold;
                    cursor: pointer;
                    letter-spacing: 2px;
                }
                @media (max-width: 768px) {
                    .date-selector {
                        flex-direction: column;
                        gap: 15px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>财富天赋罗盘</h1>
                <form action="/generate_report" method="post">
                    <div class="date-selector">
                        <div class="select-group">
                            <label for="year">年</label>
                            <select id="year" name="year" required>
                                <option value="">请选择</option>
                                <option value="2024">2024</option>
                                <option value="2023">2023</option>
                                <option value="2022">2022</option>
                                <option value="2021">2021</option>
                                <option value="2020">2020</option>
                            </select>
                        </div>
                        <div class="select-group">
                            <label for="month">月</label>
                            <select id="month" name="month" required>
                                <option value="">请选择</option>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                                <option value="5">5</option>
                                <option value="6">6</option>
                                <option value="7">7</option>
                                <option value="8">8</option>
                                <option value="9">9</option>
                                <option value="10">10</option>
                                <option value="11">11</option>
                                <option value="12">12</option>
                            </select>
                        </div>
                        <div class="select-group">
                            <label for="day">日</label>
                            <select id="day" name="day" required>
                                <option value="">请选择</option>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                                <option value="5">5</option>
                                <option value="6">6</option>
                                <option value="7">7</option>
                                <option value="8">8</option>
                                <option value="9">9</option>
                                <option value="10">10</option>
                                <option value="11">11</option>
                                <option value="12">12</option>
                                <option value="13">13</option>
                                <option value="14">14</option>
                                <option value="15">15</option>
                                <option value="16">16</option>
                                <option value="17">17</option>
                                <option value="18">18</option>
                                <option value="19">19</option>
                                <option value="20">20</option>
                                <option value="21">21</option>
                                <option value="22">22</option>
                                <option value="23">23</option>
                                <option value="24">24</option>
                                <option value="25">25</option>
                                <option value="26">26</option>
                                <option value="27">27</option>
                                <option value="28">28</option>
                                <option value="29">29</option>
                                <option value="30">30</option>
                                <option value="31">31</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="submit-button">开启罗盘</button>
                </form>
            </div>
        </body>
        </html>
        '''
    
    with open(index_path, 'r', encoding='utf-8') as f:
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
    app.run(debug=False, host='0.0.0.0', port=5002, threaded=True, use_reloader=False)
