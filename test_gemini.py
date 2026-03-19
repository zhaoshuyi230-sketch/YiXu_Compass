import google.generativeai as genai

# 配置 Google Gemini API 密钥
genai.configure(api_key="AIzaSyAb-FhQTEYXZ1Bo_M601Xr-nVRHGIuzopU")

def test_gemini_api():
    """测试 Gemini API 是否正常工作"""
    print("正在测试 Gemini API 连接...")
    
    try:
        # 创建 Gemini 模型实例
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro"
        )
        
        # 发送一个简单的测试请求
        test_prompt = "请用一句话介绍你自己。"
        response = model.generate_content(test_prompt)
        
        print("✅ API 连接成功！")
        print(f"\n模型回复：{response.text}")
        print("\n您的 Gemini API 配置正确，可以正常使用。")
        
    except Exception as e:
        print(f"❌ API 连接失败：{e}")
        print("\n请检查：")
        print("1. API 密钥是否正确")
        print("2. 网络连接是否正常")
        print("3. 是否已安装 google-generativeai 库")

if __name__ == "__main__":
    test_gemini_api()