# Hello Agent - 跟着 Datawhale 学 Agent 开发

基于 [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) 教程的学习实践项目。

## 学习路线（4周 / 30天）

| 周次 | 对应章节 | 主题 | 核心内容 |
|------|----------|------|----------|
| 第1周 | 第1-3章 | 理论基础 + LLM入门 | 智能体概念、发展史、LLM API调用 |
| 第2周 | 第4-7章 | Agent范式 + 框架 | ReAct、工具调用、自建Agent框架 |
| 第3周 | 第8-12章 | 高级技能 | 记忆系统、上下文工程、通信协议、评估 |
| 第4周 | 第13-16章 | 综合项目 | 旅行助手、深度研究、赛博小镇、毕业设计 |

> 详细路线图见 [docs/learning-roadmap.md](docs/learning-roadmap.md)

## 项目结构

```
hello-agent/
├── week1/          # 第1周：理论 + LLM 基础练习
├── week2/          # 第2周：Agent 范式 + 框架实践
├── week3/          # 第3周：高级技能练习
├── week4/          # 第4周：综合项目实战
├── docs/           # 学习笔记与路线图
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API 密钥
echo "OPENAI_API_KEY=your-key-here" > .env

# 3. 运行第一个示例
python week1/01_hello_api.py
```

## 参考资源

- 教程仓库：https://github.com/datawhalechina/hello-agents
- 在线阅读：https://datawhalechina.github.io/hello-agents/

## Git 常用命令速查

```bash
git status                    # 查看修改状态
git add 文件名                # 添加文件到暂存区
git commit -m "说明"          # 提交修改
git push                      # 推送到 GitHub
git pull                      # 拉取最新代码
```
