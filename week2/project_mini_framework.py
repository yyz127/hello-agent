"""
Day 13-14 周末项目：构建你自己的迷你 Agent 框架

对应 hello-agents 第7章：构建你的 Agent 框架

学习目标：
- 理解 Agent 框架的核心架构
- 从零实现一个可扩展的 Agent 框架
- 体验"造轮子"的学习过程

这是第2周最重要的练习！hello-agents 第7章的核心就是自建框架。
请先阅读第7章，然后参考这个骨架代码完成你自己的实现。
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import Any
from abc import ABC, abstractmethod

load_dotenv()


# ============================================================
# 1. BaseTool - 工具基类
# ============================================================

class BaseTool(ABC):
    """所有工具的基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """工具名称"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """工具描述"""
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """工具参数的 JSON Schema"""
        pass

    @abstractmethod
    def run(self, **kwargs) -> str:
        """执行工具"""
        pass

    def to_openai_tool(self) -> dict:
        """转换为 OpenAI 工具定义格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": list(self.parameters.keys()),
                }
            }
        }


# ============================================================
# 2. Memory - 记忆管理
# ============================================================

class Memory:
    """对话记忆管理器"""

    def __init__(self, max_messages: int = 50):
        self.messages: list[dict] = []
        self.max_messages = max_messages

    def add(self, message: dict):
        """添加消息"""
        self.messages.append(message)
        # 如果超出限制，移除最早的消息（保留 system 消息）
        while len(self.messages) > self.max_messages:
            # 找到第一条非 system 消息并移除
            for i, msg in enumerate(self.messages):
                if msg.get("role") != "system":
                    self.messages.pop(i)
                    break

    def get_messages(self) -> list[dict]:
        """获取所有消息"""
        return self.messages.copy()

    def clear(self):
        """清空记忆（保留 system 消息）"""
        self.messages = [m for m in self.messages if m.get("role") == "system"]

    def save(self, filepath: str):
        """保存记忆到文件"""
        # TODO: 练习 - 实现保存功能
        # 提示: 使用 json.dump 保存 self.messages
        pass

    def load(self, filepath: str):
        """从文件加载记忆"""
        # TODO: 练习 - 实现加载功能
        pass


# ============================================================
# 3. Agent - 核心 Agent 类
# ============================================================

class Agent:
    """
    迷你 Agent 框架的核心类。

    使用方式:
        agent = Agent(system_prompt="你是一个助手")
        agent.register_tool(MyTool())
        reply = agent.chat("你好")
    """

    def __init__(
        self,
        system_prompt: str = "你是一个有用的AI助手。",
        model: str = "gpt-4o-mini",
        max_iterations: int = 10,
    ):
        self.model = model
        self.max_iterations = max_iterations
        self.tools: dict[str, BaseTool] = {}
        self.memory = Memory()
        self.memory.add({"role": "system", "content": system_prompt})
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def register_tool(self, tool: BaseTool):
        """注册一个工具"""
        self.tools[tool.name] = tool
        print(f"  已注册工具: {tool.name} - {tool.description}")

    def chat(self, user_input: str) -> str:
        """
        与 Agent 对话。

        这是 Agent 的核心循环：
        1. 接收用户输入
        2. 调用 LLM
        3. 如果 LLM 要调用工具 → 执行工具 → 把结果反馈给 LLM → 回到步骤 2
        4. 如果 LLM 直接回复 → 返回回复
        """
        self.memory.add({"role": "user", "content": user_input})

        tool_definitions = [t.to_openai_tool() for t in self.tools.values()] or None

        for iteration in range(self.max_iterations):
            # 调用 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.memory.get_messages(),
                tools=tool_definitions,
            )

            assistant_msg = response.choices[0].message

            # 没有工具调用 → 直接返回回复
            if not assistant_msg.tool_calls:
                reply = assistant_msg.content or ""
                self.memory.add({"role": "assistant", "content": reply})
                return reply

            # 有工具调用 → 执行工具
            self.memory.add(assistant_msg)

            for tool_call in assistant_msg.tool_calls:
                result = self._execute_tool(tool_call)
                self.memory.add({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        return "（达到最大迭代次数）"

    def _execute_tool(self, tool_call) -> str:
        """执行单个工具调用"""
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        if func_name not in self.tools:
            return f"错误: 未知工具 '{func_name}'"

        try:
            result = self.tools[func_name].run(**func_args)
            return str(result)
        except Exception as e:
            return f"工具执行错误: {e}"

    def reset(self):
        """重置对话"""
        self.memory.clear()


# ============================================================
# 4. 示例工具实现
# ============================================================

class WeatherTool(BaseTool):
    """天气查询工具"""

    @property
    def name(self): return "get_weather"

    @property
    def description(self): return "获取城市天气信息"

    @property
    def parameters(self):
        return {"city": {"type": "string", "description": "城市名称"}}

    def run(self, city: str) -> str:
        data = {
            "北京": "晴，22°C，湿度45%",
            "上海": "多云，26°C，湿度72%",
            "广州": "雷阵雨，30°C，湿度85%",
        }
        return data.get(city, f"暂无 {city} 的天气数据")


class CalculatorTool(BaseTool):
    """计算器工具"""

    @property
    def name(self): return "calculate"

    @property
    def description(self): return "计算数学表达式"

    @property
    def parameters(self):
        return {"expression": {"type": "string", "description": "数学表达式"}}

    def run(self, expression: str) -> str:
        try:
            return str(eval(expression))
        except Exception as e:
            return f"计算错误: {e}"


# ============================================================
# 5. 运行示例
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("迷你 Agent 框架 Demo")
    print("=" * 50)

    # 创建 Agent
    agent = Agent(
        system_prompt="你是一个智能助手，可以查天气和做数学计算。请用中文简洁地回复。"
    )

    # 注册工具
    print("\n注册工具:")
    agent.register_tool(WeatherTool())
    agent.register_tool(CalculatorTool())

    # 交互式对话
    print("\n开始对话（输入 'quit' 退出）:")
    print("-" * 50)

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        if not user_input:
            continue

        reply = agent.chat(user_input)
        print(f"Agent: {reply}")


# ============================================================
# 练习题（重要！）
# ============================================================
"""
练习 1: 实现 Memory 的 save() 和 load() 方法
练习 2: 创建一个 NoteTool，能保存和读取笔记到文件
练习 3: 创建一个 TodoTool，能管理待办事项（添加、查看、删除）
练习 4: 给 Agent 添加 verbose 模式，打印每一步的详细信息
练习 5: （挑战）实现多 Agent 协作：
        创建两个 Agent，一个擅长查信息，一个擅长做总结，
        让它们协作完成一个任务
"""
