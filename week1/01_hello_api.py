"""
Day 1: Hello API - 你的第一个 Claude API 调用

学习目标：
- 理解什么是 API（应用程序编程接口）
- 学会安装和导入 Python 库
- 发送第一个请求给 Claude 并获取回复

什么是 API？
    想象 API 就像餐厅的服务员：
    你（程序）-> 告诉服务员（API）你要什么 -> 厨房（Claude）准备好 -> 服务员把结果带回来

    我们通过 API 和 Claude 对话，就像通过服务员点菜一样。
"""

# ============================================================
# 第一步：导入需要的库
# ============================================================

# anthropic 是 Claude 的官方 Python 库，帮我们方便地调用 API
import anthropic

# dotenv 帮我们从 .env 文件读取 API 密钥（密钥不应该写在代码里！）
from dotenv import load_dotenv

# os 用来读取环境变量
import os

# ============================================================
# 第二步：加载 API 密钥
# ============================================================

# 从 .env 文件加载环境变量
# .env 文件里应该有一行：ANTHROPIC_API_KEY=sk-ant-xxxxx
load_dotenv()

# 读取 API 密钥
api_key = os.getenv("ANTHROPIC_API_KEY")

# 检查密钥是否存在
if not api_key:
    print("错误：请先在 .env 文件中设置 ANTHROPIC_API_KEY")
    print("步骤：")
    print("1. 在项目根目录创建 .env 文件")
    print("2. 写入：ANTHROPIC_API_KEY=你的密钥")
    print("3. 密钥从 https://console.anthropic.com 获取")
    exit(1)

# ============================================================
# 第三步：创建客户端
# ============================================================

# 创建一个 Anthropic 客户端，用它来和 Claude 通信
# 就像打电话前先拨号建立连接
client = anthropic.Anthropic(api_key=api_key)

# ============================================================
# 第四步：发送请求
# ============================================================

print("正在向 Claude 发送请求...\n")

# 调用 Claude API 发送消息
# messages.create() 就是"发送一条消息并等待回复"
response = client.messages.create(
    # model: 选择使用哪个 Claude 模型
    # claude-sonnet-4-20250514 是一个性价比很高的模型
    model="claude-sonnet-4-20250514",

    # max_tokens: 回复的最大长度（以 token 为单位）
    # 1 个中文字大约是 1-2 个 token
    max_tokens=1024,

    # messages: 对话内容，是一个列表
    # 每条消息有 role（角色）和 content（内容）
    messages=[
        {
            "role": "user",          # "user" 表示这是用户说的话
            "content": "你好！请用一句话介绍什么是 AI Agent。"
        }
    ]
)

# ============================================================
# 第五步：处理回复
# ============================================================

# response 是 Claude 返回的完整响应对象
# response.content 是回复内容的列表（通常只有一个元素）
# response.content[0].text 是实际的文字回复
reply = response.content[0].text

print("Claude 的回复：")
print(reply)

# 我们还可以查看一些有用的信息
print(f"\n--- 额外信息 ---")
print(f"使用的模型: {response.model}")
print(f"输入 token 数: {response.usage.input_tokens}")
print(f"输出 token 数: {response.usage.output_tokens}")
print(f"停止原因: {response.stop_reason}")
# stop_reason 为 "end_turn" 表示 Claude 自然结束了回复
# 如果是 "max_tokens" 表示回复被截断了（达到了最大长度限制）


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 修改 messages 中的 content，问 Claude 不同的问题，观察回复
练习 2: 修改 max_tokens 为 50，看看回复会怎样变化
练习 3: 尝试在 messages 列表中添加多条消息，看看会发生什么
         提示: 可以交替添加 "user" 和 "assistant" 角色的消息
"""
