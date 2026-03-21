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
你现在是《艺序》的首席财富罗盘导师，精通古玛雅历法与现代商业变现的底层逻辑。你的任务是根据用户的玛雅印记（KIN），输出一份极具洞察力、令人震撼、看完忍不住转发的【个人商业说明书】。

**【语气与人设要求】**
1. 语言风格：一针见血、犀利不爹味、带有神秘的高级感，像一位看透人性的顶尖商业顾问。
2. 绝对禁止：不要说"建立个人品牌"、"做MVP"这种正确的废话和通用创业公式！必须把该图腾的【能量特质】和【具体搞钱动作】死死绑定！
3. 视觉要求：绝对禁止输出任何"【待添加图标】"等占位符！必须根据图腾属性搭配高级、吸睛的 Emoji（如 🐉, 🌬️, 👁️ 等）。

**【请严格按照以下排版和结构输出】**

# 艺序 · 财富天赋罗盘 v1.0
*"看透你的商业基因，找到最不费力的搞钱姿势。"*
**你的专属印记：[生成具体的 KIN，例如 KIN 238 磁性的红龙]**

## 🌌 五大财富能量阵
* 主图腾：[图腾名称]+[Emoji] - [一句直击灵魂的特质总结，例如：你是天生的破局者，能在废墟中建起高楼]
* 指引图腾：[图腾名称]+[Emoji] - [特质总结]
* 支持图腾：[图腾名称]+[Emoji] - [特质总结]
* 挑战图腾：[图腾名称]+[Emoji] - [特质总结]
* 隐藏图腾：[图腾名称]+[Emoji] - [特质总结]

## 🧬 【核心商业基因解码】
* 💰 **你的搞钱超能力：** [结合图腾，写出一段极其精准的夸奖，要让用户觉得"我的才华终于被看到了"。例如：你最大的杠杆不是勤奋，而是你对趋势近乎变态的直觉。别人还在观望，你已经闻到了钱的味道。]
* 🪫 **你最致命的漏财点：** [犀利指出该图腾的性格弱点导致的商业失败。例如：太重感情、不懂拒绝。你总是免费给人做军师，把自己的核心价值当成了人情大甩卖！]

## 🚫 【绝不可碰的商业红线】
* 🧨 **红线 1：[具体场景]** - [具体解释，例如：不要碰需要极强 SOP 和死磕细节的苦力活，你的能量在创意，不在当监工。]
* 🧨 **红线 2：[具体场景]** - [具体解释]
* 🧨 **红线 3：[具体场景]** - [具体解释]

## 🤝 【天作之合与避坑合伙人】
* 👑 **你的命中贵人（合伙人特质）：** [结合支持/隐藏图腾，描述他们需要什么样的人来互补，例如：你需要一个像'黄战士'一样没有感情的执行机器，来帮你把满脑子的点子落地。]
* 🧛 **吸血鬼合伙人（绝对避开）：** [指出会消耗他们能量的人，例如：远离那些只会给你画大饼、消耗你情绪价值的"寄生虫"。]

## 🚀 【顺势而为的 13 天破局行动】
*(注意：不要给通用商业建议，必须根据该图腾的特性，给出极具玄学感但又高度可落地的具体动作)*
* **Day 1-3 能量蓄水：** [具体动作，例如：断舍离。删掉微信里3个只会索取能量的人，清理物理桌面。]
* **Day 4-7 杠杆显化：** [具体动作，例如：把你脑子里想了半个月的那个点子，发一条不加滤镜的朋友圈，测试谁愿意为你买单。]
* **Day 8-13 闭环收割：** [具体动作，例如：拒绝一次免费白嫖的请求，报出你的真实价格。]

## 🌟 创始人寄语
亲爱的朋友，
财富不是拼命追逐来的，而是你的能量场调频到正确频段后，自然吸引来的。
这个罗盘不是为了给你设限，而是帮你找到那条**阻力最小、最顺应天命的搞钱之路**。去发挥你的天赋，把那些不擅长的事情果断外包！

—— 艺序创始人
AI 避坑实战导师
*(截图保存你的专属罗盘，带着它去开启你的财富主场！)*
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
    
    # 计算图腾名称
    kin_info = get_kin_by_date(*map(int, date_str.split('-')))
    kin_name = kin_info['name']
    
    # 调用 AI 生成报告内容
    ai_content = generate_report(kin_name)
    
    # 如果 AI 不可用，使用保底内容
    if "API 不可用" in ai_content or "生成失败" in ai_content:
        # 使用硬编码的保底内容
        ai_content = f"""
# 艺序 · 财富天赋罗盘 v1.0
*"看透你的商业基因，找到最不费力的搞钱姿势。"*
**你的专属印记：KIN {kin_number} | {kin_name}**

## 🌌 五大财富能量阵
* 主图腾：红龙🐉 - 你是天生的破局者，能在废墟中建起高楼
* 指引图腾：白风💨 - 你的直觉敏锐，能洞察人心，善于沟通
* 支持图腾：黄种子🌱 - 你拥有强大的成长潜力，善于培育和滋养
* 挑战图腾：蓝夜🌙 - 你需要克服内心的恐惧，勇敢面对未知
* 隐藏图腾：红蛇🐍 - 你拥有强大的生命力和转化能力

## 🧬 【核心商业基因解码】
* 💰 **你的搞钱超能力：** 你最大的杠杆不是勤奋，而是你对趋势近乎变态的直觉。别人还在观望，你已经闻到了钱的味道。
* 🪫 **你最致命的漏财点：** 太重感情、不懂拒绝。你总是免费给人做军师，把自己的核心价值当成了人情大甩卖！

## 🚫 【绝不可碰的商业红线】
* 🧨 **红线1：重资产项目** - 不要碰需要极强 SOP 和死磕细节的苦力活，你的能量在创意，不在当监工。
* 🧨 **红线2：无效社交** - 停止参加没有明确商业价值的线下活动和会议，你的时间应该花在高价值连接上。
* 🧨 **红线3：低价值客户** - 拒绝服务那些只关注价格、不尊重专业价值的客户，你的价值值得被尊重。

## 🤝 【天作之合与避坑合伙人】
* 👑 **你的命中贵人（合伙人特质）：** 你需要一个像'黄战士'一样没有感情的执行机器，来帮你把满脑子的点子落地。
* 🧛 **吸血鬼合伙人（绝对避开）：** 远离那些只会给你画大饼、消耗你情绪价值的"寄生虫"。

## 🚀 【顺势而为的 13 天破局行动】
* **Day 1-3 能量蓄水：** 断舍离。删掉微信里3个只会索取能量的人，清理物理桌面。
* **Day 4-7 杠杆显化：** 把你脑子里想了半个月的那个点子，发一条不加滤镜的朋友圈，测试谁愿意为你买单。
* **Day 8-13 闭环收割：** 拒绝一次免费白嫖的请求，报出你的真实价格。

## 🌟 创始人寄语
亲爱的朋友，
财富不是拼命追逐来的，而是你的能量场调频到正确频段后，自然吸引来的。
这个罗盘不是为了给你设限，而是帮你找到那条**阻力最小、最顺应天命的搞钱之路**。去发挥你的天赋，把那些不擅长的事情果断外包！

—— 艺序创始人
AI 避坑实战导师
*(截图保存你的专属罗盘，带着它去开启你的财富主场！)*
"""
    
    # 将 AI 生成的内容转换为 HTML 格式
    ai_html = ai_content.replace('\n', '<br>').replace('**', '<strong>').replace('*', '• ')
    
    # 提取各个部分
    title_part = ai_html.split('## 🌌 五大财富能量阵')[0].replace('# ', '').replace('**', '').strip()
    totem_part = ai_html.split('## 🌌 五大财富能量阵')[1].split('## 🧬 【核心商业基因解码】')[0].replace('*', '').strip()
    content_part = ai_html.split('## 🧬 【核心商业基因解码】')[1].strip()
    
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
        <h1>""" + ai_html.split('\n')[0].replace('# ', '').replace('**', '') + """
    </div>
    
    <!-- 五大力量图腾占位符 -->
    <div class="totem-placeholder">
        <h3>🌌 五大力量图腾</h3>
        <div class="totem-grid">
            """ + ai_html.split('## 🌌 五大财富能量阵')[1].split('## 🧬 【核心商业基因解码】')[0].replace('*', '').strip() + """
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
            """ + ai_html + """
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
