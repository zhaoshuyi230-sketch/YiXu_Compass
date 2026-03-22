import os

# 测试文件路径
print("=== 测试文件路径 ===")
print("当前目录:", os.getcwd())
print("index.html 存在:", os.path.exists("index.html"))
print("pay_qr.jpg 存在:", os.path.exists("pay_qr.jpg"))

# 测试绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("\n=== 绝对路径测试 ===")
print("BASE_DIR:", BASE_DIR)
print("index.html 绝对路径:", os.path.join(BASE_DIR, "index.html"))
print("index.html 绝对路径存在:", os.path.exists(os.path.join(BASE_DIR, "index.html")))
print("pay_qr.jpg 绝对路径:", os.path.join(BASE_DIR, "pay_qr.jpg"))
print("pay_qr.jpg 绝对路径存在:", os.path.exists(os.path.join(BASE_DIR, "pay_qr.jpg")))

# 测试读取文件
print("\n=== 测试读取文件 ===")
try:
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        print("index.html 读取成功，长度:", len(content))
except Exception as e:
    print("index.html 读取失败:", str(e))

try:
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        content = f.read()
        print("index.html 绝对路径读取成功，长度:", len(content))
except Exception as e:
    print("index.html 绝对路径读取失败:", str(e))