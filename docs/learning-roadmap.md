# 基于 Datawhale hello-agents 的一个月学习路线图

> 参考教程：[datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)
> 在线阅读：https://datawhalechina.github.io/hello-agents/

## 教程简介

hello-agents 是 Datawhale 社区的开源智能体学习教程，共 **16 章**，分为 5 大部分：

| 部分 | 章节 | 内容 |
|------|------|------|
| 第一部分：基础理论 | 第1-3章 | 智能体概念、发展史、LLM基础 |
| 第二部分：实战开发 | 第4-7章 | 经典范式、低代码平台、框架开发、自建框架 |
| 第三部分：高级技能 | 第8-12章 | 记忆系统、上下文工程、通信协议、模型训练、评估 |
| 第四部分：综合项目 | 第13-15章 | 旅行助手、深度研究Agent、赛博小镇 |
| 第五部分：毕业设计 | 第16章 | 综合设计 |

---

## 前置准备（Day 0）

### 你需要准备的
- Python 3.10+ 已安装
- 一个代码编辑器（推荐 VS Code）
- OpenAI API Key（hello-agents 教程基于 OpenAI API）
- GitHub 账号

### 环境搭建
```bash
# 1. 克隆 hello-agents 教程仓库（作为参考资料）
git clone https://github.com/datawhalechina/hello-agents.git ~/hello-agents-tutorial

# 2. 进入你的练习项目
cd hello-agent

# 3. 创建虚拟环境
python -m venv venv

# 4. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt
```

### Git 基础操作速查
```bash
git status                    # 查看哪些文件被修改了
git add 文件名                # 把修改的文件加入暂存区
git add .                     # 把所有修改的文件加入暂存区
git commit -m "说明做了什么"   # 提交修改（保存一个版本）
git push                      # 推送到 GitHub
git pull                      # 从 GitHub 拉取最新代码
git log --oneline             # 查看提交历史
```

---

## 第1周：理论基础 + LLM 入门（Day 1-7）

> 对应 hello-agents 第1-3章

### 学习目标
- 理解什么是智能体（Agent），它和普通聊天机器人有什么区别
- 了解智能体的发展历史和不同类型
- 掌握大语言模型（LLM）的基本使用方法

### 每日计划

#### Day 1 - 初识智能体（第1章）
- **阅读**: hello-agents 第1章 - 智能体的定义与组成
- **核心概念**:
  - 什么是 Agent？→ 能感知环境、自主决策、执行行动的系统
  - Agent 的核心组件：感知、规划、记忆、行动
  - Agent vs 普通聊天机器人的区别
- **练习**: `week1/01_hello_api.py` - 先学会调用 LLM API

#### Day 2 - 智能体发展史（第2章）
- **阅读**: hello-agents 第2章
- **核心概念**:
  - 从规则系统 → 专家系统 → 强化学习 Agent → LLM Agent 的演变
  - ReAct、CoT、Tool Use 等关键范式
- **练习**: `week1/02_message_format.py` - 理解消息格式

#### Day 3-4 - LLM 基础（第3章上）
- **阅读**: hello-agents 第3章（前半部分）
- **核心概念**:
  - Transformer 架构基本理解（不需要数学细节）
  - Token、上下文窗口、temperature 等核心概念
  - Prompt Engineering 基础
- **练习**: `week1/03_parameters.py` + `week1/05_prompt_engineering.py`

#### Day 5-6 - LLM 实践（第3章下）
- **阅读**: hello-agents 第3章（后半部分）
- **核心概念**:
  - API 调用的完整流程
  - 流式输出（Streaming）
  - System Prompt 设计
- **练习**: `week1/04_streaming.py` + `week1/project_translator.py`

#### Day 7 - 周日复习
- 回顾第1-3章核心概念
- 完成翻译器项目的扩展练习
- **Git 练习**: 把本周代码提交并推送

---

## 第2周：Agent 经典范式 + 框架实践（Day 8-14）

> 对应 hello-agents 第4-7章

### 学习目标
- 理解 ReAct、CoT 等经典 Agent 范式
- 学会使用主流 Agent 框架
- 能从零构建一个简单的 Agent 框架

### 每日计划

#### Day 8-9 - 经典范式构建（第4章）
- **阅读**: hello-agents 第4章
- **核心概念**:
  - ReAct 范式：推理（Reasoning）+ 行动（Acting）
  - CoT（思维链）：让 Agent 一步步思考
  - 工具调用（Tool Use）的基本原理
- **练习**: `week2/01_react_pattern.py` - 实现简单的 ReAct 循环
- **练习**: `week2/02_tool_use_basics.py` - 第一个工具调用

#### Day 10 - 低代码平台体验（第5章）
- **阅读**: hello-agents 第5章
- **核心概念**:
  - 了解 Coze、Dify 等低代码平台
  - 理解可视化搭建 Agent 的思路
- **动手**: 在 Coze 或 Dify 上搭建一个简单 Agent（可选）
- **笔记**: `week2/03_notes_lowcode.md` - 记录体验和对比

#### Day 11-12 - 框架开发实践（第6章）
- **阅读**: hello-agents 第6章
- **核心概念**:
  - 主流框架介绍（LangChain、AutoGen 等）
  - 框架的核心抽象：Chain、Agent、Tool、Memory
- **练习**: `week2/04_framework_practice.py` - 用框架构建 Agent

#### Day 13-14 - 构建你的 Agent 框架（第7章）
- **阅读**: hello-agents 第7章（重点章节！）
- **核心概念**:
  - 自己动手设计 Agent 框架的架构
  - 工具注册、消息管理、执行循环
- **项目**: `week2/project_mini_framework.py` - 构建迷你 Agent 框架
  - 实现工具注册机制
  - 实现 Agent 主循环（感知→思考→行动）
  - 实现简单的记忆管理

---

## 第3周：高级技能（Day 15-21）

> 对应 hello-agents 第8-12章

### 学习目标
- 掌握 Agent 的记忆与检索系统
- 理解上下文工程（Context Engineering）
- 了解 Agent 通信协议和评估方法

### 每日计划

#### Day 15-16 - 记忆与检索（第8章）
- **阅读**: hello-agents 第8章
- **核心概念**:
  - 短期记忆 vs 长期记忆
  - 向量数据库与语义检索（RAG）
  - 记忆的存储、检索和遗忘策略
- **练习**: `week3/01_memory_system.py` - 实现记忆系统
- **练习**: `week3/02_simple_rag.py` - 简单的 RAG 实现

#### Day 17 - 上下文工程（第9章）
- **阅读**: hello-agents 第9章
- **核心概念**:
  - 如何管理有限的上下文窗口
  - 信息压缩、摘要策略
  - 动态上下文构建
- **练习**: `week3/03_context_engineering.py`

#### Day 18 - Agent 通信协议（第10章）
- **阅读**: hello-agents 第10章
- **核心概念**:
  - MCP（Model Context Protocol）
  - Agent 之间如何通信协作
  - 标准化协议的意义
- **练习**: `week3/04_agent_communication.py`

#### Day 19 - Agentic-RL 概览（第11章）
- **阅读**: hello-agents 第11章
- **核心概念**:
  - 强化学习在 Agent 中的应用
  - 奖励设计、策略优化
- **笔记**: `week3/05_notes_agentic_rl.md` - 理论为主，记录理解

#### Day 20-21 - Agent 评估（第12章）
- **阅读**: hello-agents 第12章
- **核心概念**:
  - 如何评估 Agent 的性能
  - 评估指标：准确性、效率、鲁棒性
  - 基准测试（Benchmark）
- **练习**: `week3/project_evaluation.py` - 为之前的 Agent 写评估

---

## 第4周：综合项目实战（Day 22-30）

> 对应 hello-agents 第13-16章

### 学习目标
- 完成 2-3 个完整的 Agent 项目
- 整合前三周所有知识
- 完成一个可展示的毕业设计

### 每日计划

#### Day 22-23 - 智能旅行助手（第13章）
- **阅读**: hello-agents 第13章
- **项目**: `week4/travel_assistant/`
  - 接收旅行需求（目的地、天数、预算）
  - 规划行程路线
  - 推荐景点和餐厅
  - 生成详细旅行计划

#### Day 24-26 - 自动化深度研究 Agent（第14章）
- **阅读**: hello-agents 第14章
- **项目**: `week4/deep_research/`
  - 接收研究主题
  - 分解研究问题
  - 搜索和收集信息
  - 整理、分析和总结
  - 生成结构化研究报告

#### Day 27-28 - 赛博小镇（第15章）
- **阅读**: hello-agents 第15章
- **项目**: `week4/cyber_town/`（简化版）
  - 多个 Agent 模拟小镇居民
  - Agent 之间的对话和互动
  - 观察涌现行为

#### Day 29-30 - 毕业设计（第16章）
- **阅读**: hello-agents 第16章
- **项目**: `week4/final_project/` - 选择一个方向深入：
  - 选项 A：增强版旅行助手（加入实时搜索、地图集成）
  - 选项 B：个人知识库 Agent（RAG + 工具调用）
  - 选项 C：自定义主题的 Agent（根据你的兴趣）

---

## 学习建议

### 每天的学习流程
1. **阅读教程章节** - 在 hello-agents 在线文档或 PDF 中阅读理论
2. **看配套代码** - 参考 hello-agents 的 `code/` 目录
3. **动手练习** - 在本项目中完成对应练习
4. **修改实验** - 改参数、改提示词，观察变化
5. **Git 提交** - 养成保存进度的习惯

### 阅读顺序
- 理论部分（第1-3章）可以快速阅读，重点理解概念
- 实战部分（第4-7章）需要慢慢跟着代码做
- 高级部分（第8-12章）选择性深入，不用每章都精通
- 项目部分（第13-16章）重点动手，边做边学

### 遇到问题怎么办
- **代码报错** → 仔细阅读错误信息，复制到搜索引擎查询
- **概念不懂** → 回看 hello-agents 对应章节，或问 Claude
- **API 问题** → 检查 API Key 和网络连接
- **Git 问题** → 参考 README 中的 Git 速查表

### 每周 Git 工作流
```bash
# 每天开始前
git pull

# 完成一个练习后
git add .
git commit -m "完成 Day X: 练习名称"

# 每天结束时推送
git push
```
