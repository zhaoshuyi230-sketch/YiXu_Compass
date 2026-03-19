#!/usr/bin/env python3
"""模拟生成 KIN 206 报告，测试升级后的内容质量"""

import maya_kin

# 模拟 KIN 206 的详细信息
kin_206_details = {
    'kin': 206,
    'date': '2024-01-15',
    'tone': '宇宙',
    'tone_number': 13,
    'glyph': '白世界桥',
    'glyph_number': 6,
    'castle': '绿色城堡',
    'castle_key': 'green',
    'family': '极性家族',
    'sop': '白色周',
    'sop_key': 'white'
}

# 测试生成分析内容
print("=" * 60)
print("正在模拟生成 KIN 206 白世界桥 - 宇宙调性 报告...")
print("=" * 60)
print()

# 构建测试用的 topic 和 details
topic = "KIN 206 白世界桥 - 宇宙调性 - 绿色城堡 - 极性家族"
details = f"""
印记信息：
- KIN编号：{kin_206_details['kin']}
- 调性：{kin_206_details['tone']}（{kin_206_details['tone_number']}）
- 图腾：{kin_206_details['glyph']}（{kin_206_details['glyph_number']}）
- 城堡：{kin_206_details['castle']}
- 家族：{kin_206_details['family']}
- SOP：{kin_206_details['sop']}

白世界桥特质：连接、机会、均等、死亡与重生
宇宙调性特质：存在、安忍、超越、当下
绿色城堡特质：心轮、共时、魔法、转化
极性家族特质：建立极性、定义方向、确立目标
"""

# 调用 generate_analysis 函数
try:
    analysis = maya_kin.generate_analysis(topic, details)
    print("✅ 报告生成成功！")
    print()
    print("=" * 60)
    print("【KIN 206 白世界桥 - 宇宙调性】商业分析报告")
    print("=" * 60)
    print()
    print(analysis)
    print()
    print("=" * 60)
    print("报告生成完成")
    print("=" * 60)
except Exception as e:
    print(f"❌ 报告生成失败: {e}")