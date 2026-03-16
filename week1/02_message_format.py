"""
Day 2: 消息格式 - 理解 Claude 的对话结构

学习目标：
- 理解 system、user、assistant 三种角色
- 学会使用 system prompt 设定 AI 的行为
- 了解消息列表的结构

核心概念：
    Claude 的对话由三种角色组成：
    - system（系统）: 给 AI 的"幕后指令"，用户看不到，定义 AI 的行为规则
    - user（用户）: 用户说的话
    - assistant（助手）: AI 的回复
"""

import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ============================================================
# 示例 1：没有 system prompt
# ============================================================

print("=" * 50)
print("示例 1：没有 system prompt")
print("=" * 50)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "1+1等于几？"}
    ]
)
print(response.content[0].text)


# ============================================================
# 示例 2：使用 system prompt 定义角色
# ============================================================

print("\n" + "=" * 50)
print("示例 2：使用 system prompt（数学老师）")
print("=" * 50)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    # system 参数：设定 AI 的角色和行为
    # 这就像给演员一个"角色说明书"
    system="你是一位耐心的小学数学老师。回答问题时要用简单易懂的语言，并举生活中的例子。",
    messages=[
        {"role": "user", "content": "1+1等于几？"}
    ]
)
print(response.content[0].text)


# ============================================================
# 示例 3：使用 system prompt 定义另一个角色
# ============================================================

print("\n" + "=" * 50)
print("示例 3：使用 system prompt（海盗）")
print("=" * 50)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    system="你是一个说话像海盗的AI。每句话都要加上海盗风格的表达，比如'啊哈'、'宝藏'等。",
    messages=[
        {"role": "user", "content": "1+1等于几？"}
    ]
)
print(response.content[0].text)


# ============================================================
# 示例 4：模拟多轮对话（提供历史消息）
# ============================================================

print("\n" + "=" * 50)
print("示例 4：模拟多轮对话")
print("=" * 50)

# 通过提供之前的对话历史，Claude 可以理解上下文
# 注意：user 和 assistant 必须交替出现
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        # 第一轮对话
        {"role": "user", "content": "我叫小明。"},
        {"role": "assistant", "content": "你好小明！很高兴认识你！"},

        # 第二轮对话 - Claude 应该记得"小明"这个名字
        {"role": "user", "content": "你还记得我叫什么吗？"},
    ]
)
print(response.content[0].text)
# Claude 应该回答"小明"，因为对话历史中包含了这个信息


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 创建一个"诗人"角色的 system prompt，让 Claude 用诗歌形式回答问题
练习 2: 创建一个3轮对话的消息列表，让 Claude 记住你告诉它的信息
练习 3: 尝试让 system prompt 控制输出格式，比如"每次回答都用列表形式"
"""
