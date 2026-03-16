"""
第1周项目：智能翻译器

这是第一周的综合练习项目，整合了你学到的所有知识：
- API 调用
- System Prompt
- 参数调优
- 流式输出

功能：
1. 自动检测输入语言
2. 中英互译
3. 可选翻译风格（正式/口语/文学）
4. 流式输出翻译结果
"""

import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def translate(text, style="正式"):
    """
    翻译函数：自动检测语言并翻译。

    参数:
        text: 要翻译的文本
        style: 翻译风格 - "正式"、"口语"、"文学"
    """
    # 根据风格选择不同的 system prompt
    style_prompts = {
        "正式": "使用正式、专业的语言风格翻译。",
        "口语": "使用口语化、自然的日常对话风格翻译。",
        "文学": "使用优美、富有文学色彩的语言翻译。",
    }

    style_instruction = style_prompts.get(style, style_prompts["正式"])

    system_prompt = f"""你是一个专业的翻译助手。
规则：
1. 自动检测输入语言
2. 如果输入是中文，翻译成英文；如果输入是英文，翻译成中文
3. {style_instruction}
4. 先输出"[检测语言: XX -> XX]"，然后换行输出翻译结果
5. 只输出翻译结果，不要添加解释"""

    print(f"\n翻译中（{style}风格）...\n")

    # 使用流式输出
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        temperature=0.3,  # 翻译任务用较低温度，保证准确性
        system=system_prompt,
        messages=[{"role": "user", "content": text}]
    ) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
    print()  # 换行


def main():
    """主函数：运行交互式翻译器"""
    print("=" * 50)
    print("   智能翻译器 v1.0")
    print("   输入文本即可翻译（中英互译）")
    print("   命令：")
    print("     /style 正式|口语|文学  - 切换风格")
    print("     /quit                  - 退出")
    print("=" * 50)

    current_style = "正式"

    while True:
        # 获取用户输入
        print()
        text = input("请输入要翻译的文本: ").strip()

        # 处理命令
        if not text:
            continue
        if text == "/quit":
            print("再见！")
            break
        if text.startswith("/style"):
            parts = text.split()
            if len(parts) > 1 and parts[1] in ["正式", "口语", "文学"]:
                current_style = parts[1]
                print(f"已切换到{current_style}风格")
            else:
                print("可选风格：正式、口语、文学")
            continue

        # 执行翻译
        translate(text, style=current_style)


# ============================================================
# 运行翻译器
# ============================================================
if __name__ == "__main__":
    main()


# ============================================================
# 扩展练习
# ============================================================
"""
练习 1: 添加更多语言支持（日语、韩语等）
练习 2: 添加"解释模式"，翻译后解释关键词汇和语法
练习 3: 添加翻译历史记录功能，把结果保存到文件
"""
