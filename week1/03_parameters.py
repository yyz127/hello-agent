"""
Day 3: 参数调优 - 控制 Claude 的输出行为

学习目标：
- 理解 temperature 参数（创造性 vs 确定性）
- 理解 max_tokens 参数（回复长度控制）
- 学会根据场景选择合适的参数

核心概念：
    temperature（温度）:
    - 值范围：0.0 ~ 1.0
    - 低温（0.0）：回答更确定、更一致，适合事实性问题
    - 高温（1.0）：回答更多样、更有创意，适合创作类任务

    max_tokens（最大令牌数）:
    - 控制回复的最大长度
    - 1个中文字 ≈ 1-2个 token
    - 设太小会导致回复被截断
"""

import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def ask_claude(question, temperature=1.0, max_tokens=256):
    """
    封装 API 调用为一个函数，方便复用。

    参数:
        question: 要问的问题
        temperature: 温度参数，控制随机性
        max_tokens: 最大回复长度
    返回:
        Claude 的回复文本
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.content[0].text


# ============================================================
# 实验 1：temperature 对事实性问题的影响
# ============================================================

print("=" * 50)
print("实验 1：事实性问题 + 不同 temperature")
print("=" * 50)

question = "中国的首都是哪里？"

# 低温度：回答更确定
print(f"\ntemperature=0.0:")
print(ask_claude(question, temperature=0.0))

# 高温度：回答可能更发散
print(f"\ntemperature=1.0:")
print(ask_claude(question, temperature=1.0))


# ============================================================
# 实验 2：temperature 对创作性任务的影响
# ============================================================

print("\n" + "=" * 50)
print("实验 2：创作性任务 + 不同 temperature")
print("=" * 50)

question = "用一句话描述春天。"

# 低温度：更常规的描述
print(f"\ntemperature=0.0:")
print(ask_claude(question, temperature=0.0))

# 中等温度
print(f"\ntemperature=0.5:")
print(ask_claude(question, temperature=0.5))

# 高温度：更有创意的描述
print(f"\ntemperature=1.0:")
print(ask_claude(question, temperature=1.0))


# ============================================================
# 实验 3：max_tokens 的影响
# ============================================================

print("\n" + "=" * 50)
print("实验 3：不同 max_tokens")
print("=" * 50)

question = "请详细介绍 Python 编程语言。"

# 很短的限制
print(f"\nmax_tokens=30:")
reply = ask_claude(question, max_tokens=30)
print(reply)
print("（注意：回复可能被截断）")

# 较长的限制
print(f"\nmax_tokens=200:")
print(ask_claude(question, max_tokens=200))


# ============================================================
# 实验 4：多次调用同一问题，观察一致性
# ============================================================

print("\n" + "=" * 50)
print("实验 4：同一问题多次调用（temperature=0.0）")
print("=" * 50)

question = "给我一个1到10之间的数字。"

print("temperature=0.0（应该每次都一样）:")
for i in range(3):
    print(f"  第{i+1}次: {ask_claude(question, temperature=0.0)}")

print("\ntemperature=1.0（可能每次不同）:")
for i in range(3):
    print(f"  第{i+1}次: {ask_claude(question, temperature=1.0)}")


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 写一个函数，接受"创作模式"或"精确模式"参数，
        自动设置合适的 temperature
练习 2: 找到一个问题，在不同 temperature 下回答差异最大
练习 3: 实验找出描述"春天"需要的最少 max_tokens 是多少
"""
