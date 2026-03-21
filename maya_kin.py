import os
from openai import OpenAI
import datetime

# 1. 初始化 DeepSeek 客户端（使用你在 Vercel 填的暗号）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url="https://api.deepseek.com/v1"
)

# 2. 满血版核心 Prompt
SYSTEM_PROMPT = """
你现在是《艺序》的首席职场能量教练与资深商业心理分析师。你的任务是根据用户的【玛雅印记 (KIN)】，生成一份极具洞察力、能引发用户强烈共鸣并主动转发的《个人商业出厂说明书》。
（...此处省略你那段超长的 Prompt 文本，粘贴时请保留完整内容...）
"""

# 3. 这里的函数是给 app.py 调用的“发动机”
def generate_report(kin_name):
    try:
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
