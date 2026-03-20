import os
from openai import OpenAI

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
    return {"name": "磁性的蓝夜", "number": 183}