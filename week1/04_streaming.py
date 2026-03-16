"""
Day 4: 流式输出 - 像打字机一样逐字显示

学习目标：
- 理解流式响应（Streaming）的概念
- 实现实时逐字显示效果
- 了解流式和非流式的区别

核心概念：
    普通请求：等 Claude 想完整个回答，一次性返回（可能等很久）
    流式请求：Claude 边想边返回，一个字一个字地传给你（体验更好）

    就像看直播（流式）vs 看录播（非流式）的区别。
"""

import anthropic
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ============================================================
# 示例 1：普通请求（非流式）
# ============================================================

print("=" * 50)
print("示例 1：普通请求（等待完整回复）")
print("=" * 50)

start_time = time.time()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    messages=[
        {"role": "user", "content": "写一首关于编程的短诗，4行。"}
    ]
)

elapsed = time.time() - start_time
print(response.content[0].text)
print(f"\n（等待 {elapsed:.1f} 秒后一次性显示）")


# ============================================================
# 示例 2：流式请求（逐字显示）
# ============================================================

print("\n" + "=" * 50)
print("示例 2：流式请求（逐字显示）")
print("=" * 50)

start_time = time.time()

# 使用 stream=True 开启流式模式
# 使用 with 语句确保连接正确关闭
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    messages=[
        {"role": "user", "content": "写一首关于编程的短诗，4行。"}
    ]
) as stream:
    # stream.text_stream 是一个迭代器，逐块返回文本
    for text in stream.text_stream:
        # end="" 表示不换行，flush=True 表示立即显示
        print(text, end="", flush=True)

elapsed = time.time() - start_time
print(f"\n\n（流式传输，总耗时 {elapsed:.1f} 秒，但第一个字很快就显示了）")


# ============================================================
# 示例 3：流式请求 + 收集完整回复
# ============================================================

print("\n" + "=" * 50)
print("示例 3：流式显示的同时收集完整回复")
print("=" * 50)

collected_text = ""  # 用来收集完整文本

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "用3个要点介绍Python的优势。"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
        collected_text += text  # 同时收集到变量中

print("\n")
print(f"收集到的完整文本长度: {len(collected_text)} 字符")
# 现在 collected_text 里有完整的回复，可以后续使用


# ============================================================
# 示例 4：获取流式响应的最终统计信息
# ============================================================

print("\n" + "=" * 50)
print("示例 4：流式响应 + 统计信息")
print("=" * 50)

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "Python 是什么？一句话回答。"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    # stream 结束后，可以获取最终的响应对象
    final_response = stream.get_final_message()

print(f"\n\n输入 tokens: {final_response.usage.input_tokens}")
print(f"输出 tokens: {final_response.usage.output_tokens}")


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 用流式输出实现一个"打字机效果"，每个字之间加 0.05 秒延迟
        提示: 在 print 后加 time.sleep(0.05)
练习 2: 实现一个函数，支持传入 streaming=True/False 参数来切换模式
练习 3: 用流式模式让 Claude 写一个长故事（500字），
        同时统计总共收到了多少个文本块（chunk）
"""
