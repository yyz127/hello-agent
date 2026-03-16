"""
Day 11-12: 框架开发实践

对应 hello-agents 第6章：框架开发实践

学习目标：
- 了解 Agent 框架的核心概念
- 理解框架帮我们做了什么
- 为第7章自建框架做准备

核心概念：
    为什么需要框架？
    前面我们手动写了 ReAct 循环和工具调用，代码比较多且重复。
    框架帮我们把这些通用的模式封装好了，让我们专注于业务逻辑。

    一个 Agent 框架通常包含：
    1. Tool（工具）- 定义 Agent 能做什么
    2. Memory（记忆）- 管理对话历史
    3. Agent（智能体）- 核心推理和决策逻辑
    4. Chain/Pipeline - 组合多个步骤
"""

# ============================================================
# 这个文件演示如何用简单的模式组织 Agent 代码
# 即使不用第三方框架，好的代码组织也很重要
# ============================================================

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import Callable

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# 1. 工具层：用装饰器注册工具
# ============================================================

# 工具注册表
_tool_registry = {}


def tool(name: str, description: str, parameters: dict):
    """
    工具注册装饰器。

    用法:
        @tool("get_weather", "获取天气", {"city": {"type": "string"}})
        def get_weather(city: str):
            return {"temp": 25}
    """
    def decorator(func):
        _tool_registry[name] = {
            "function": func,
            "definition": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": parameters,
                        "required": list(parameters.keys()),
                    }
                }
            }
        }
        return func
    return decorator


# 注册工具 —— 只需要加装饰器，非常简洁

@tool("get_weather", "获取城市天气", {
    "city": {"type": "string", "description": "城市名称"}
})
def get_weather(city: str):
    data = {
        "北京": "晴，22°C",
        "上海": "多云，26°C",
        "广州": "雷阵雨，30°C",
    }
    return data.get(city, f"暂无 {city} 的天气数据")


@tool("calculate", "计算数学表达式", {
    "expression": {"type": "string", "description": "数学表达式"}
})
def calculate(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"


# ============================================================
# 2. 简单 Agent 类
# ============================================================

class SimpleAgent:
    """一个简单的 Agent 框架实现"""

    def __init__(self, system_prompt: str, model: str = "gpt-4o-mini"):
        self.system_prompt = system_prompt
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]

    def run(self, user_input: str) -> str:
        """处理用户输入并返回回复"""
        self.messages.append({"role": "user", "content": user_input})

        # Agent 循环
        max_iterations = 5
        for _ in range(max_iterations):
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=[t["definition"] for t in _tool_registry.values()] if _tool_registry else None,
            )

            assistant_msg = response.choices[0].message

            # 如果不需要工具调用，返回文本回复
            if not assistant_msg.tool_calls:
                reply = assistant_msg.content
                self.messages.append({"role": "assistant", "content": reply})
                return reply

            # 处理工具调用
            self.messages.append(assistant_msg)

            for tool_call in assistant_msg.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                # 查找并执行工具
                if func_name in _tool_registry:
                    result = _tool_registry[func_name]["function"](**func_args)
                else:
                    result = f"未知工具: {func_name}"

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })

        return "达到最大迭代次数"

    def reset(self):
        """清空对话历史"""
        self.messages = [{"role": "system", "content": self.system_prompt}]


# ============================================================
# 运行示例
# ============================================================

if __name__ == "__main__":
    # 创建 Agent
    agent = SimpleAgent(
        system_prompt="你是一个智能助手，可以查天气和做计算。请用中文回复。"
    )

    # 测试对话
    questions = [
        "北京天气怎么样？",
        "帮我算 123 * 456",
        "你好，你能做什么？",
    ]

    for q in questions:
        print(f"\n用户: {q}")
        reply = agent.run(q)
        print(f"Agent: {reply}")

    print("\n\n--- 使用框架的好处 ---")
    print("1. 工具注册只需要加 @tool 装饰器")
    print("2. Agent 循环逻辑被封装在 SimpleAgent 类中")
    print("3. 添加新工具不需要修改 Agent 代码")
    print("4. 对话历史自动管理")


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 给 SimpleAgent 添加一个 history 属性，返回对话历史的摘要
练习 2: 添加 save/load 方法，将对话历史保存到 JSON 文件
练习 3: 创建你自己的工具（比如 "翻译"、"生成摘要" 等）
练习 4: 阅读 hello-agents 第7章，把这个简单框架扩展为更完整的版本
"""
