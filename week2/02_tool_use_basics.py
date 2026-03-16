"""
Day 9: 工具调用基础 - 使用 OpenAI Function Calling

对应 hello-agents 第4章：智能体经典范式构建

学习目标：
- 理解 Function Calling（工具调用）的标准机制
- 学会用 JSON Schema 定义工具
- 掌握工具调用的完整流程

核心概念：
    上一个文件我们手动解析了 "Action: xxx" 这样的文本格式。
    但现代 LLM API 提供了标准的 Function Calling 机制：
    1. 你告诉 LLM 有哪些工具（用 JSON Schema 描述）
    2. LLM 决定是否调用工具，并返回结构化的调用请求
    3. 你执行工具，把结果返回给 LLM
    4. LLM 基于结果生成最终回答

    这比手动解析文本可靠得多！
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# 第一步：定义工具函数
# ============================================================

def get_weather(city: str) -> dict:
    """
    获取城市天气（模拟数据）。
    在真实项目中，你会调用天气 API。
    """
    # 模拟天气数据
    weather_data = {
        "北京": {"temperature": 22, "condition": "晴", "humidity": 45},
        "上海": {"temperature": 26, "condition": "多云", "humidity": 72},
        "广州": {"temperature": 30, "condition": "雷阵雨", "humidity": 85},
        "深圳": {"temperature": 29, "condition": "阴", "humidity": 78},
    }
    if city in weather_data:
        return weather_data[city]
    return {"error": f"暂不支持查询 {city} 的天气"}


def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"


# ============================================================
# 第二步：用 JSON Schema 描述工具
# ============================================================

# OpenAI Function Calling 要求用 JSON Schema 定义工具的参数格式
# 这让 LLM 知道每个工具需要什么输入

tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",                    # 工具名称
            "description": "获取指定城市的天气信息",     # 工具描述（帮助 LLM 判断何时使用）
            "parameters": {                           # 参数定义（JSON Schema 格式）
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'、'上海'"
                    }
                },
                "required": ["city"]                  # 必填参数
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 工具名称到函数的映射
tool_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
}


# ============================================================
# 第三步：实现工具调用循环
# ============================================================

def chat_with_tools(user_message: str):
    """
    与带工具的 Agent 对话。

    完整流程：
    1. 发送用户消息和工具定义给 LLM
    2. LLM 可能返回工具调用请求
    3. 执行工具，把结果返回给 LLM
    4. LLM 生成最终回复
    """
    print(f"\n用户: {user_message}")

    messages = [
        {"role": "system", "content": "你是一个有用的助手，可以查询天气和做数学计算。"},
        {"role": "user", "content": user_message}
    ]

    # 第一次调用：LLM 决定是否使用工具
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tool_definitions,    # 传入工具定义
    )

    assistant_message = response.choices[0].message

    # 检查 LLM 是否决定调用工具
    if assistant_message.tool_calls:
        print(f"Agent 决定调用工具...")

        # 把 assistant 的消息加入历史（包含工具调用信息）
        messages.append(assistant_message)

        # 处理每个工具调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"  调用工具: {function_name}({function_args})")

            # 执行对应的工具函数
            if function_name in tool_functions:
                result = tool_functions[function_name](**function_args)
            else:
                result = f"未知工具: {function_name}"

            print(f"  工具返回: {result}")

            # 把工具结果加入消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,      # 关联到具体的工具调用
                "content": json.dumps(result, ensure_ascii=False),
            })

        # 第二次调用：LLM 基于工具结果生成最终回复
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        final_reply = response.choices[0].message.content
    else:
        # LLM 认为不需要工具，直接回复
        final_reply = assistant_message.content

    print(f"Agent: {final_reply}")
    return final_reply


# ============================================================
# 运行示例
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("示例 1：需要查天气的问题")
    print("=" * 60)
    chat_with_tools("北京今天天气怎么样？")

    print("\n" + "=" * 60)
    print("示例 2：需要计算的问题")
    print("=" * 60)
    chat_with_tools("帮我算一下 (15 * 23 + 47) / 3 等于多少？")

    print("\n" + "=" * 60)
    print("示例 3：不需要工具的问题")
    print("=" * 60)
    chat_with_tools("你好，请介绍一下你自己。")

    print("\n" + "=" * 60)
    print("示例 4：需要多个工具的问题")
    print("=" * 60)
    chat_with_tools("上海和广州今天的天气如何？温度差多少度？")


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 添加一个 "get_date" 工具，返回今天的日期
练习 2: 修改 get_weather 函数，让它支持更多城市
练习 3: 实现一个交互式循环，让用户持续和 Agent 对话
        提示: while True + input()
练习 4: 尝试用 Anthropic 的 Claude API 实现同样的功能
        Claude 的工具调用格式和 OpenAI 稍有不同，查阅文档对比
"""
