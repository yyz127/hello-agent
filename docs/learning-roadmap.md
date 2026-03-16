# Agent 开发学习路线图（一个月）

## 前置准备（Day 0）

### 你需要准备的
- Python 3.10+ 已安装
- 一个代码编辑器（推荐 VS Code）
- Anthropic API Key（从 https://console.anthropic.com 获取）
- GitHub 账号（你已经有了）

### 环境搭建
```bash
# 进入项目目录
cd hello-agent

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

## 第1周：Python基础 & API入门（Day 1-7）

### 学习目标
- 理解 API 调用的基本概念
- 学会使用 Claude API 发送请求和处理响应
- 掌握 Python 函数、字典、列表等基础知识

### 每日计划

#### Day 1 - Hello API
- **学习**: 什么是 API？什么是 LLM？
- **练习**: `week1/01_hello_api.py` - 发送第一个 API 请求
- **知识点**: API Key、HTTP 请求、JSON 格式

#### Day 2 - 理解消息格式
- **学习**: Claude 消息格式（role、content）
- **练习**: `week1/02_message_format.py` - 不同角色的消息
- **知识点**: system/user/assistant 角色、消息列表

#### Day 3 - 参数调优
- **学习**: temperature、max_tokens 等参数含义
- **练习**: `week1/03_parameters.py` - 实验不同参数效果
- **知识点**: 模型参数对输出的影响

#### Day 4 - 流式输出
- **学习**: 什么是流式响应（Streaming）
- **练习**: `week1/04_streaming.py` - 实现打字机效果
- **知识点**: 流式 API、事件处理

#### Day 5 - 提示词工程基础
- **学习**: 如何写好 System Prompt
- **练习**: `week1/05_prompt_engineering.py` - 不同提示词对比
- **知识点**: 角色设定、输出格式控制、Few-shot

#### Day 6-7 - 周末练习
- **复习**: 回顾本周所有代码
- **项目**: `week1/project_translator.py` - 做一个简单的翻译器
- **扩展**: 尝试修改参数，观察不同结果

---

## 第2周：对话式 Agent（Day 8-14）

### 学习目标
- 理解多轮对话的实现原理
- 学会管理对话历史（记忆）
- 构建一个有个性的聊天 Agent

### 每日计划

#### Day 8 - 多轮对话
- **学习**: 对话上下文是如何维护的
- **练习**: `week2/01_multi_turn.py` - 实现多轮对话
- **知识点**: 消息列表的累积、上下文窗口

#### Day 9 - 对话记忆管理
- **学习**: 长对话的记忆策略
- **练习**: `week2/02_memory.py` - 实现滑动窗口记忆
- **知识点**: Token 限制、记忆截断策略

#### Day 10 - 对话保存与加载
- **学习**: 文件读写（JSON）
- **练习**: `week2/03_save_load.py` - 对话存档功能
- **知识点**: JSON 序列化、文件操作

#### Day 11 - 角色扮演 Agent
- **学习**: 通过 System Prompt 定义 Agent 人格
- **练习**: `week2/04_persona_agent.py` - 创建角色扮演Agent
- **知识点**: 人格设计、行为约束

#### Day 12 - 结构化输出
- **学习**: 让 Agent 返回结构化数据
- **练习**: `week2/05_structured_output.py` - JSON 模式输出
- **知识点**: 输出解析、JSON Schema

#### Day 13-14 - 周末项目
- **项目**: `week2/project_tutor.py` - AI 学习助手
- 功能：记住学习进度、个性化教学、保存笔记

---

## 第3周：工具调用 Agent（Day 15-21）

### 学习目标
- 理解 Function Calling（工具调用）机制
- 学会定义和实现自定义工具
- 构建能"做事"的 Agent

### 每日计划

#### Day 15 - 工具调用基础
- **学习**: 什么是 Tool Use / Function Calling
- **练习**: `week3/01_tool_basics.py` - 第一个工具调用
- **知识点**: 工具定义格式、工具调用流程

#### Day 16 - 计算器工具
- **学习**: 多工具定义与选择
- **练习**: `week3/02_calculator.py` - Agent + 计算器
- **知识点**: 工具参数定义、结果返回

#### Day 17 - 文件操作工具
- **学习**: Agent 操作本地文件
- **练习**: `week3/03_file_tools.py` - 读写文件的Agent
- **知识点**: 安全考虑、权限控制

#### Day 18 - 网络搜索工具
- **学习**: Agent 调用外部 API
- **练习**: `week3/04_web_tools.py` - 能搜索的Agent
- **知识点**: API 集成、错误处理

#### Day 19 - 工具链与多步推理
- **学习**: Agent 连续调用多个工具
- **练习**: `week3/05_tool_chain.py` - 多步骤任务
- **知识点**: Agent Loop、思维链

#### Day 20-21 - 周末项目
- **项目**: `week3/project_assistant.py` - 个人助理Agent
- 功能：查天气、做计算、记笔记、管理待办

---

## 第4周：综合实战（Day 22-30）

### 学习目标
- 整合所有知识构建完整 Agent 系统
- 学习错误处理和健壮性
- 完成一个可展示的 Agent 项目

### 每日计划

#### Day 22 - 错误处理
- **学习**: API 错误、工具执行错误的处理
- **练习**: `week4/01_error_handling.py`
- **知识点**: try/except、重试机制、优雅降级

#### Day 23 - Agent 架构设计
- **学习**: Agent 的设计模式
- **练习**: `week4/02_agent_class.py` - 面向对象的Agent
- **知识点**: 类、继承、设计模式

#### Day 24 - 多 Agent 协作
- **学习**: 多个 Agent 分工合作
- **练习**: `week4/03_multi_agent.py`
- **知识点**: Agent 编排、任务分发

#### Day 25 - Agent 评估
- **学习**: 如何测试和评估 Agent
- **练习**: `week4/04_evaluation.py`
- **知识点**: 测试用例、评估指标

#### Day 26-30 - 毕业项目
- **项目**: `week4/final_project/` - 智能研究助手
- 功能：
  - 接收研究主题
  - 搜索和收集信息
  - 整理和总结内容
  - 生成结构化报告
  - 支持追问和深入研究

---

## 学习建议

### 每天的学习流程
1. **阅读代码注释** - 每个文件都有详细的中文注释
2. **运行示例** - 先运行看效果
3. **修改实验** - 改参数、改提示词，观察变化
4. **完成练习** - 每个文件末尾都有练习题
5. **Git 提交** - 养成保存进度的习惯

### 遇到问题怎么办
- 代码报错 → 仔细阅读错误信息，大多数错误信息都说明了原因
- 概念不懂 → 代码中有注释解释，也可以问 Claude
- API 问题 → 检查 API Key 是否配置正确

### Git 工作流（每天）
```bash
# 开始学习前，拉取最新代码
git pull

# 学习过程中，随时保存
git add .
git commit -m "完成 Day X: 主题名称"

# 学习结束后，推送到远程
git push
```
