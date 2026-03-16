# Hello Agent - Agent 开发学习项目

这是一个从零开始学习 AI Agent 开发的实践项目，使用 Python + Claude API 构建。

## 学习路线（4周）

| 周次 | 主题 | 核心内容 |
|------|------|----------|
| 第1周 | Python基础 & 环境搭建 | API调用、函数、模块 |
| 第2周 | 对话式Agent | 多轮对话、系统提示词、记忆管理 |
| 第3周 | 工具调用Agent | Function Calling、工具定义与编排 |
| 第4周 | 完整Agent项目 | 多工具协作、错误处理、实战项目 |

## 项目结构

```
hello-agent/
├── week1/          # 第1周：基础篇
├── week2/          # 第2周：对话Agent
├── week3/          # 第3周：工具调用
├── week4/          # 第4周：综合项目
├── docs/           # 学习笔记与文档
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置API密钥（创建 .env 文件）
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# 3. 运行第一个示例
python week1/01_hello_api.py
```

## Git 常用命令速查

```bash
# 查看当前状态
git status

# 添加修改的文件
git add 文件名

# 提交修改
git commit -m "描述你做了什么"

# 推送到远程
git push

# 拉取最新代码
git pull
```
