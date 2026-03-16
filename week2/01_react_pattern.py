"""
Day 8-9: ReAct 范式 - 让 Agent 边思考边行动

对应 hello-agents 第4章：智能体经典范式构建

学习目标：
- 理解 ReAct (Reasoning + Acting) 范式
- 实现一个简单的 ReAct Agent 循环
- 理解 Agent 和普通 LLM 调用的区别

核心概念：
    普通 LLM 调用：用户提问 → LLM 回答（一问一答）
    ReAct Agent：用户提问 → LLM 思考 → 决定行动 → 执行工具 → 观察结果 → 继续思考 → ... → 最终回答

    ReAct 循环：
    1. Thought（思考）：我应该怎么做？
    2. Action（行动）：调用某个工具
    3. Observation（观察）：工具返回了什么
    4. 重复直到得出最终答案
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# 第一步：定义工具（Agent 可以使用的能力）
# ============================================================

def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        # 注意：eval 在生产环境中不安全，这里仅用于学习
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"


def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 工具注册表：名称 -> 函数的映射
tools = {
    "calculate": calculate,
    "get_current_time": get_current_time,
}

# 工具描述（告诉 LLM 有哪些工具可用）
tools_description = """
你可以使用以下工具：

1. calculate(expression) - 计算数学表达式
   例如: calculate("2 + 3 * 4")

2. get_current_time() - 获取当前时间

当你需要使用工具时，请用以下格式：
Thought: [你的思考过程]
Action: [工具名称]
Action Input: [工具参数]

当你得到工具的结果后，会以 Observation: [结果] 的形式呈现。

当你已经得到最终答案时，请用：
Thought: 我已经得到了答案
Final Answer: [最终回答]
"""


# ============================================================
# 第二步：实现 ReAct 循环
# ============================================================

def run_react_agent(user_question: str, max_steps: int = 5):
    """
    运行一个简单的 ReAct Agent。

    参数:
        user_question: 用户的问题
        max_steps: 最大推理步数（防止无限循环）
    """
    print(f"\n{'='*50}")
    print(f"用户问题: {user_question}")
    print(f"{'='*50}\n")

    # 构建初始消息
    system_prompt = f"""你是一个智能助手，可以使用工具来帮助回答问题。
{tools_description}

请一步步思考，必要时使用工具来获取信息。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]

    for step in range(max_steps):
        print(f"--- 步骤 {step + 1} ---")

        # 调用 LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 可替换为你能使用的模型
            messages=messages,
            temperature=0,
        )

        assistant_reply = response.choices[0].message.content
        print(assistant_reply)

        # 检查是否有最终答案
        if "Final Answer:" in assistant_reply:
            final_answer = assistant_reply.split("Final Answer:")[-1].strip()
            print(f"\n{'='*50}")
            print(f"最终答案: {final_answer}")
            print(f"{'='*50}")
            return final_answer

        # 检查是否需要调用工具
        if "Action:" in assistant_reply and "Action Input:" in assistant_reply:
            # 解析工具调用
            action_line = [l for l in assistant_reply.split("\n") if l.startswith("Action:")][0]
            input_line = [l for l in assistant_reply.split("\n") if l.startswith("Action Input:")][0]

            tool_name = action_line.replace("Action:", "").strip()
            tool_input = input_line.replace("Action Input:", "").strip()

            # 执行工具
            if tool_name in tools:
                if tool_input:
                    observation = tools[tool_name](tool_input)
                else:
                    observation = tools[tool_name]()
                print(f"Observation: {observation}\n")
            else:
                observation = f"错误: 未知工具 '{tool_name}'"
                print(f"Observation: {observation}\n")

            # 把 LLM 的回复和工具结果加入消息历史
            messages.append({"role": "assistant", "content": assistant_reply})
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            # 如果既没有 Final Answer 也没有 Action，直接返回
            print(f"\n{'='*50}")
            print(f"Agent 回复: {assistant_reply}")
            print(f"{'='*50}")
            return assistant_reply

    print("达到最大步数限制，Agent 停止。")
    return None


# ============================================================
# 运行示例
# ============================================================

if __name__ == "__main__":
    # 示例 1：需要计算的问题
    run_react_agent("一个苹果 3.5 元，买 7 个苹果，再加上 8% 的税，总共多少钱？")

    # 示例 2：需要获取时间的问题
    run_react_agent("现在几点了？")

    # 示例 3：不需要工具的问题
    run_react_agent("什么是人工智能？用一句话回答。")


# ============================================================
# 练习题
# ============================================================
"""
练习 1: 添加一个新工具 "string_length(text)"，返回字符串的长度
练习 2: 让 Agent 处理需要连续调用两个工具的问题
        例如："现在几点了？如果把小时数乘以分钟数等于多少？"
练习 3: 添加工具调用的错误处理，当工具执行失败时让 Agent 重新选择策略
"""
