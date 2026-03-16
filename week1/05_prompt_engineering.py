"""
Day 5: 提示词工程 - 让 Claude 更好地理解你的意图

学习目标：
- 掌握写好提示词的关键技巧
- 理解 Few-shot（少样本示例）的用法
- 学会控制输出格式

核心概念：
    提示词工程就是"学会怎么跟 AI 说话"。
    同样的问题，不同的问法，会得到截然不同的回答。

    关键技巧：
    1. 明确角色 - 告诉 AI 它是谁
    2. 明确任务 - 告诉 AI 要做什么
    3. 给出示例 - 告诉 AI 你想要什么样的输出
    4. 指定格式 - 告诉 AI 用什么格式回答
"""

import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def ask(system_prompt, user_message, max_tokens=512):
    """简单的 API 调用封装"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text


# ============================================================
# 技巧 1：明确角色和任务
# ============================================================

print("=" * 50)
print("技巧 1：明确角色和任务")
print("=" * 50)

# 模糊的提示
print("\n模糊提示:")
print(ask("", "说说Python"))

# 明确的提示
print("\n明确提示:")
print(ask(
    "你是一位有5年经验的Python开发者，擅长教初学者。",
    "请用3个要点介绍Python的核心优势，每个要点用一句话说明。"
))


# ============================================================
# 技巧 2：Few-shot 少样本示例
# ============================================================

print("\n" + "=" * 50)
print("技巧 2：Few-shot 少样本示例")
print("=" * 50)

# Few-shot: 在提示中给出输入-输出的示例，让 Claude 学习规律
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        # 示例 1
        {"role": "user", "content": "把这个句子翻译成英文并标注情感：今天天气真好！"},
        {"role": "assistant", "content": "翻译: The weather is really nice today!\n情感: 积极 😊"},

        # 示例 2
        {"role": "user", "content": "把这个句子翻译成英文并标注情感：我的手机坏了。"},
        {"role": "assistant", "content": "翻译: My phone is broken.\n情感: 消极 😢"},

        # 真正的问题 - Claude 会模仿上面的格式回答
        {"role": "user", "content": "把这个句子翻译成英文并标注情感：周末我要去爬山。"},
    ]
)
print("Few-shot 结果:")
print(response.content[0].text)


# ============================================================
# 技巧 3：控制输出格式
# ============================================================

print("\n" + "=" * 50)
print("技巧 3：控制输出格式")
print("=" * 50)

# 让 Claude 输出 JSON 格式
print("\nJSON 格式输出:")
print(ask(
    "你是一个数据分析助手。所有回复必须是有效的 JSON 格式。不要输出其他任何内容。",
    '分析这句话的情感："今天学到了很多新知识，感觉很充实！"'
))

# 让 Claude 输出表格格式
print("\n表格格式输出:")
print(ask(
    "你是一个信息整理助手。用 Markdown 表格格式回答所有问题。",
    "对比 Python、JavaScript、Java 这三门语言的特点。"
))


# ============================================================
# 技巧 4：分步思考（Chain of Thought）
# ============================================================

print("\n" + "=" * 50)
print("技巧 4：分步思考")
print("=" * 50)

# 直接问
print("\n直接问:")
print(ask("", "一个农场有鸡和兔，共35个头，94只脚，问鸡和兔各多少只？"))

# 要求分步思考
print("\n要求分步思考:")
print(ask(
    "",
    "一个农场有鸡和兔，共35个头，94只脚，问鸡和兔各多少只？\n\n请一步一步思考，展示你的推理过程。"
))


# ============================================================
# 技巧 5：限制和约束
# ============================================================

print("\n" + "=" * 50)
print("技巧 5：限制和约束")
print("=" * 50)

print(ask(
    """你是一个Python代码助手。
规则：
1. 只回答Python相关问题
2. 代码必须包含注释
3. 回答长度不超过10行
4. 如果问题和Python无关，礼貌地拒绝""",
    "怎么用Python读取一个文件？"
))


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 设计一个 system prompt，让 Claude 扮演一个"代码审查员"，
        能指出代码中的问题并给出改进建议
练习 2: 用 Few-shot 技巧，教 Claude 把自然语言转换成 SQL 查询
        比如 "找出年龄大于18的所有用户" -> "SELECT * FROM users WHERE age > 18"
练习 3: 设计一个 system prompt，让 Claude 的回答始终包含：
        摘要、详细解释、示例代码、注意事项 四个部分
"""
