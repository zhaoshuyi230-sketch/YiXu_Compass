import os
from openai import OpenAI
import datetime
import httpx

# 1. 初始化 DeepSeek 客户端（使用你在 Vercel 填的暗号）
try:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"), 
        base_url="https://api.deepseek.com/v1",
        http_client=httpx.Client()
    )
    API_AVAILABLE = True
except Exception as e:
    print(f"API 初始化失败: {e}")
    print("将使用保底模式运行")
    API_AVAILABLE = False

# 2. 满血版核心 Prompt
SYSTEM_PROMPT = """
你现在是《艺序》的首席职场能量教练与资深商业心理分析师。你的任务是根据用户的【玛雅印记 (KIN)】，生成一份极具洞察力、能引发用户强烈共鸣并主动转发的《个人商业出厂说明书》。
（...此处省略你那段超长的 Prompt 文本，粘贴时请保留完整内容...）
"""

# 3. 这里的函数是给 app.py 调用的“发动机”
def generate_report(kin_name):
    try:
        if not API_AVAILABLE:
            return "API 不可用，使用保底内容"
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"请为玛雅印记【{kin_name}】生成专属的《个人商业出厂说明书》。"}
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败，原因：{str(e)}"

# 4. 玛雅印记计算逻辑（确保这个函数名和你在 app.py 里调用的 get_kin_by_date 一致）
def get_kin_by_date(year, month, day):
    # 这里放你之前的玛雅计算逻辑代码
    # 示例返回：
    # 玛雅印记计算逻辑 - 基于卓尔金历 (Tzolkin) 260天周期
    # 基准日期：2024年1月1日 = kin 114 (行星的白色巫师)
    
    # 卓尔金历两个周期
    seal_cycle = [
        "红龙", "白风", "蓝夜", "黄种子", "红蛇",
        "白世界桥", "蓝手", "黄星星", "红月", "白狗",
        "蓝猴", "黄人", "红天行者", "白巫师", "蓝鹰",
        "黄战士", "红地球", "白镜", "蓝风暴", "黄太阳"
    ]  # 20个太阳图腾
    
    tone_cycle = ["磁性", "月亮", "电力", "自我存在", "超频", 
                  "韵律", "共振", "银河", "太阳", "行星", 
                  "光谱", "水晶", "宇宙"]  # 13个银河音阶
    
    # 基准日期设置
    base_date = (2024, 1, 1)
    base_kin_number = 114  # 行星的白色巫师
    
    # 计算输入日期与基准日期的天数差
    input_date = datetime.date(year, month, day)
    base = datetime.date(*base_date)
    delta_days = (input_date - base).days
    
    # 计算目标kin编号 (1-260循环)
    target_kin = ((base_kin_number - 1 + delta_days) % 260) + 1
    
    # 计算音阶 (1-13)
    tone_index = ((target_kin - 1) % 13)
    tone = tone_cycle[tone_index]
    
    # 计算太阳图腾 (1-20)
    seal_index = ((target_kin - 1) % 20)
    seal = seal_cycle[seal_index]
    
    # 组合kin名称
    kin_name = f"{tone}的{seal}"
    
    return {"name": kin_name, "number": target_kin}

# 其他必要的函数
def get_kin_details(date_str):
    # 解析日期字符串
    try:
        year, month, day = map(int, date_str.split('-'))
        kin_info = get_kin_by_date(year, month, day)
        return {
            'kin': kin_info['number'],
            'main_id': (kin_info['number'] - 1) % 20 + 1,
            'tone_id': (kin_info['number'] - 1) % 13 + 1,
            'guide_id': (kin_info['number'] - 1) % 20 + 1,
            'challenge_id': ((kin_info['number'] - 1) % 20 + 9) % 20 + 1,
            'support_id': 21 - ((kin_info['number'] - 1) % 20 + 1),
            'hidden_id': 21 - ((kin_info['number'] - 1) % 20 + 1)
        }
    except Exception as e:
        print(f"获取 kin 详情失败: {e}")
        return {
            'kin': 1,
            'main_id': 1,
            'tone_id': 1,
            'guide_id': 1,
            'challenge_id': 1,
            'support_id': 1,
            'hidden_id': 1
        }

def build_report(date_str):
    details = get_kin_details(date_str)
    kin_number = details.get('kin', 0)
    
    # 将所有需要用到的名字和Key提前计算好
    glyph_name = "红龙"  # 简化处理，实际应该从映射表中获取
    tone_name = "磁性"  # 简化处理，实际应该从映射表中获取
    guide_name = "白风"  # 简化处理，实际应该从映射表中获取
    challenge_name = "蓝夜"  # 简化处理，实际应该从映射表中获取
    support_name = "黄种子"  # 简化处理，实际应该从映射表中获取
    hidden_name = "红蛇"  # 简化处理，实际应该从映射表中获取
    
    # 修复后的城堡和SOP key计算
    castle_key = "green"  # 简化处理
    sop_key = "white"  # 简化处理
    
    # 使用普通字符串拼接，避免 f-string 中的大括号冲突
    html = """
    <html>
    <head>
        <title>财富天赋罗盘 - KIN """ + str(kin_number) + """</title>
        <meta charset="UTF-8">
        <!-- 【UI换装】黑金高端版CSS -->
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
                line-height: 1.8;
                margin: 0;
                padding: 0;
                background-color: #1a1a1a;
                color: #d4af37;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 30px;
                background-color: #141414;
                border-bottom: 1px solid #d4af37;
                position: sticky;
                top: 0;
                z-index: 100;
            }
            .header-left {
                font-size: 1.2em;
                font-weight: bold;
                color: #d4af37;
            }
            .header-right {
                font-size: 1em;
                color: #a9a9a9;
            }
            .container {
                padding: 30px;
            }
            .energy-overview {
                margin-bottom: 30px;
                padding: 30px;
                background-color: #1e1e1e;
                border: 1px solid #d4af37;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            }
            .energy-overview h1 {
                color: #d4af37;
                font-size: 3em;
                margin: 0;
                text-shadow: 0 0 15px #d4af37;
            }
            .totem-placeholder {
                margin: 30px 0;
                padding: 40px;
                background-color: #242424;
                border: 2px solid #d4af37;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            }
            .totem-placeholder h3 {
                color: #d4af37;
                margin-bottom: 20px;
            }
            .totem-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .totem-item {
                padding: 20px;
                background-color: #2a2a2a;
                border: 1px solid #d4af37;
                border-radius: 10px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            .totem-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
            }
            .totem-item h4 {
                color: #d4af37;
                margin-bottom: 10px;
            }
            .section {
                margin-bottom: 25px;
                padding: 25px;
                border: 1px solid #d4af37;
                border-radius: 10px;
                background-color: rgba(20, 20, 20, 0.8);
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                opacity: 0;
                transform: translateY(20px);
                animation: fadeIn 0.8s ease forwards;
            }
            @keyframes fadeIn {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            h2 {
                color: #d4af37;
                border-bottom: 2px solid #d4af37;
                padding-bottom: 10px;
                font-size: 1.8em;
            }
            h3 {
                color: #d4af37;
                margin-top: 20px;
                margin-bottom: 15px;
                font-size: 1.4em;
            }
            .content-text {
                color: #a9a9a9;
                font-size: 1.1em;
            }
            ul {
                list-style-type: disc;
                margin-left: 20px;
                margin-bottom: 20px;
            }
            li {
                margin-bottom: 10px;
            }
            strong {
                color: #d4af37;
            }
            .founder-message {
                margin-top: 40px;
                padding: 30px;
                background-color: #1e1e1e;
                border: 1px solid #d4af37;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            }
            .founder-message h2 {
                color: #d4af37;
                margin-bottom: 20px;
            }
            .founder-signature {
                margin-top: 20px;
                font-style: italic;
                color: #d4af37;
            }
            .export-section {
                margin-top: 40px;
                text-align: center;
            }
            .export-button {
                position: relative;
                padding: 18px 40px;
                background: linear-gradient(135deg, #d4af37 0%, #a67c00 100%);
                border: none;
                border-radius: 8px;
                color: #1a1a1a;
                font-size: 1.2em;
                font-weight: bold;
                cursor: pointer;
                overflow: hidden;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            }
            .export-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5);
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.8);
                backdrop-filter: blur(5px);
            }
            .modal-content {
                background-color: #141414;
                margin: 15% auto;
                padding: 40px;
                border: 1px solid #d4af37;
                border-radius: 15px;
                width: 90%;
                max-width: 500px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }
            .modal-content h2 {
                color: #d4af37;
                margin-bottom: 20px;
            }
            .qr-code {
                margin: 30px 0;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                display: inline-block;
            }
            .qr-code img {
                width: 200px;
                height: 200px;
            }
            .close-button {
                background-color: #d4af37;
                color: #1a1a1a;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
    <div class="header">
        <div class="header-left">艺序 · 财富天赋罗盘 v1.0</div>
        <div class="header-right">AI 避坑实战出品</div>
    </div>
    <div class="container">
    <div class="energy-overview">
        <h1>KIN """ + str(kin_number) + """ | """ + tone_name + """的""" + glyph_name + """
    </div>
    
    <!-- 五大力量图腾占位符 -->
    <div class="totem-placeholder">
        <h3>🌌 五大力量图腾</h3>
        <div class="totem-grid">
            <div class="totem-item">
                <h4>主图腾</h4>
                <p>""" + glyph_name + """
                <p>【待添加玛雅原版图标】</p>
            </div>
            <div class="totem-item">
                <h4>指引图腾</h4>
                <p>""" + guide_name + """
                <p>【待添加玛雅原版图标】</p>
            </div>
            <div class="totem-item">
                <h4>支持图腾</h4>
                <p>""" + support_name + """
                <p>【待添加玛雅原版图标】</p>
            </div>
            <div class="totem-item">
                <h4>挑战图腾</h4>
                <p>""" + challenge_name + """
                <p>【待添加玛雅原版图标】</p>
            </div>
            <div class="totem-item">
                <h4>隐藏图腾</h4>
                <p>""" + hidden_name + """
                <p>【待添加玛雅原版图标】</p>
            </div>
        </div>
    </div>
    
    <!-- 支付提示模态框 -->
    <div id="paymentModal" class="modal">
        <div class="modal-content">
            <h2>内测期间，打赏 19.9 元即可解锁高清蓝图</h2>
            <div class="qr-code">
                <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Chinese%20WeChat%20payment%20QR%20code%20for%2019.9%20yuan%2C%20professional%20design%2C%20high%20quality&image_size=square_hd" alt="收款码">
            </div>
            <p>扫描上方二维码支付后，点击下方按钮下载 PDF</p>
            <button class="close-button" onclick="closeModalAndPrint()">确认支付并下载</button>
        </div>
    </div>
    
    <!-- 商业基因板块 -->
    <div class="section">
        <h2>【商业基因】</h2>
        <div class="content-text">
            <ul>
                <li><strong>财富增长模型：</strong>轻资产+高毛利+可复制，通过知识变现和个人品牌构建实现指数增长</li>
                <li><strong>核心竞争力：</strong>独特的商业直觉和执行力，擅长在混乱中发现机会并快速验证</li>
                <li><strong>最佳定位：</strong>成为细分领域的意见领袖，通过内容输出和咨询服务建立权威</li>
            </ul>
        </div>
    </div>
    
    <!-- 避坑红线板块 -->
    <div class="section">
        <h2>【避坑红线】</h2>
        <div class="content-text">
            <ul>
                <li><strong>红线1：重资产项目</strong> - 绝对不能碰需要大额前期投入、长周期回报的项目</li>
                <li><strong>红线2：无效社交</strong> - 停止参加没有明确商业价值的线下活动和会议</li>
                <li><strong>红线3：低价值客户</strong> - 拒绝服务那些只关注价格、不尊重专业价值的客户</li>
            </ul>
        </div>
    </div>
    
    <!-- 合伙人尾数板块 -->
    <div class="section">
        <h2>【合伙人尾数】</h2>
        <div class="content-text">
            <ul>
                <li><strong>最佳尾数：</strong>4（黄种子）、8（黄星星）、12（黄人），这些数字代表系统化和执行能力</li>
                <li><strong>互补特质：</strong>你负责战略和创意，合伙人负责系统搭建和运营执行</li>
                <li><strong>权力边界：</strong>决策权重60/40，财务透明，每月定期审计</li>
            </ul>
        </div>
    </div>
    
    <!-- 13天SOP板块 -->
    <div class="section">
        <h2>【13天 SOP】</h2>
        <div class="content-text">
            <ul>
                <li><strong>Day 1：</strong>盘点个人核心能力，列出3个可变现的技能</li>
                <li><strong>Day 2-3：</strong>设计最小可行性产品(MVP)，聚焦一个核心痛点</li>
                <li><strong>Day 4-5：</strong>建立个人品牌视觉系统，包括Logo和个人形象</li>
                <li><strong>Day 6-7：</strong>创建3-5个高质量内容，定位目标客户群体</li>
                <li><strong>Day 8-9：</strong>寻找3个种子用户，免费提供服务换取反馈</li>
                <li><strong>Day 10-11：</strong>根据反馈迭代产品，调整定价策略</li>
                <li><strong>Day 12-13：</strong>制定销售漏斗，准备正式发售</li>
            </ul>
        </div>
    </div>
    
    <!-- 创始人寄语 -->
    <div class="founder-message">
        <h2>🌟 创始人寄语</h2>
        <p>亲爱的朋友，</p>
        <p>财富不是偶然，而是一种能量的显化。每一个玛雅印记都承载着独特的商业密码，等待着被唤醒。</p>
        <p>这套「财富天赋罗盘」系统，融合了玛雅历法的古老智慧与现代商业思维，旨在帮助你发现自己的财富天赋，避开商业陷阱，找到最匹配的合作伙伴，制定清晰的行动路径。</p>
        <p>记住，你的财富天赋是与生俱来的，关键在于如何将其系统化、产品化，让更多人能够从中受益。</p>
        <p>愿你在商业道路上，既有洞察先机的智慧，又有落地执行的勇气。</p>
        <div class="founder-signature">
            <p>—— 艺序创始人</p>
            <p>AI 避坑实战导师</p>
        </div>
    </div>
    
    <div class="export-section">
        <button class="export-button" onclick="openPaymentModal()">获取专属商业蓝图 PDF</button>
    </div>
    </div>
    
    <script>
        // 打开支付模态框
        function openPaymentModal() {
            document.getElementById('paymentModal').style.display = 'block';
        }
        
        // 关闭模态框并打印
        function closeModalAndPrint() {
            document.getElementById('paymentModal').style.display = 'none';
            // 等待模态框关闭后执行打印
            setTimeout(function() {
                window.print();
            }, 500);
        }
        
        // 点击模态框外部关闭
        window.onclick = function(event) {
            var modal = document.getElementById('paymentModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
        
        // 监听打印事件，确保样式正确
        window.onbeforeprint = function() {
            // 确保所有动画已完成
            var sections = document.querySelectorAll('.section');
            sections.forEach(function(section) {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            });
        };
    </script>
    </body></html>
    """
    
    print("\n--- ✅ 199元黑金版报告已生成！ ---")
    return html
