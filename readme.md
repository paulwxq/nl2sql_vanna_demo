# NL2SQL Demo

基于Python 3.12、LangChain、Vanna、LLM、pgvector和Embedding的自然语言转SQL(NL2SQL)演示项目。

## 项目简介

本项目实现了一个自然语言转SQL的系统，允许用户使用自然语言查询数据库。系统基于RAG(检索增强生成)技术，使用LLM生成SQL查询，并支持通过反馈不断优化查询结果。

## 技术栈

- Python 3.12
- LangChain：用于构建LLM应用程序
- Vanna：专注于自然语言转SQL的工具
- LLM：DeepSeek或QWEN（需提供API接入信息）
- PostgreSQL + pgvector：数据库和向量存储
- 阿里云Embedding模型：用于文本向量化

## 功能特性

- 将自然语言问题转换为SQL查询
- 执行生成的SQL并返回结果
- 支持用户反馈，持续改进查询质量
- 基于AdventureWorks风格的示例数据库
- Web界面，方便用户交互
- 支持简单、条件过滤、多表连接和复杂聚合查询

## 快速开始

### 环境准备

1. Python 3.12
2. PostgreSQL数据库（开启pgvector扩展）
3. 访问DeepSeek或QWEN模型的API密钥
4. 访问阿里云Embedding模型的API密钥

### 安装

### 1. 克隆代码仓库

git clone https://github.com/yourusername/nl2sql_demo.git
cd nl2sql_demo

### 2.创建并激活虚拟环境

bashpython -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

### 3.安装依赖

bashpip install -r requirements.txt

### 4.配置环境变量

复制.env.example文件为.env，并填写相关配置信息。
bashcp .env.example .env


### 数据库设置
使用提供的脚本创建并初始化示例数据库：
bashpython scripts/setup_db.py


### 生成训练数据
使用提供的脚本生成训练数据：
bashpython scripts/generate_training_data.py

### 启动应用
启动Web应用：
bashpython web/app.py
访问 http://localhost:5000 即可使用Web界面。


### 测试
运行单元测试：
bashpytest


### 生成训练数据集
些训练数据被包含在 scripts/generate_training_data.py 文件中，该脚本会生成四类查询示例并将它们保存到 data/training/ 目录下的JSON文件中：

simple_queries.json - 简单查询示例（如"列出所有客户"）
filter_queries.json - 条件过滤查询示例（如"查找名为John的客户"）
join_queries.json - 连接查询示例（如"显示每个订单的客户名称"）
complex_queries.json - 复杂查询示例（如"查找购买金额最高的前5名客户"）

在生成的脚本中，每个文件都包含了5个示例查询，每个查询包含了自然语言问题和对应的SQL查询。
如果您想扩展这些训练数据，可以：

修改 generate_training_data.py 文件添加更多示例
运行该脚本生成更新后的JSON文件
使用 app/vanna/trainer.py 中的 VannaTrainer 类来训练您的Vanna实例

对于AdventureWorks风格的数据库，这些示例查询应该能够很好地覆盖基本场景。如果您有特定领域的查询需求，可以根据实际业务场景扩展训练数据。











nl2sql_demo/
├── .gitignore                     # Git忽略文件
├── README.md                      # 项目说明文档
├── requirements.txt               # 项目依赖
├── setup.py                       # 包安装脚本
├── .env.example                   # 环境变量示例
├── main.py                        # 主入口文件
│
├── app/                           # 应用核心代码
│   ├── __init__.py
│   ├── config.py                  # 配置文件（LLM、Embedding API等）
│   ├── db/                        # 数据库相关
│   │   ├── __init__.py
│   │   ├── connection.py          # 数据库连接管理
│   │   └── security.py            # SQL安全过滤器
│   │
│   ├── langchain/                 # LangChain相关代码
│   │   ├── __init__.py
│   │   ├── chains.py              # 自定义链
│   │   └── llm_config.py          # LLM配置
│   │
│   ├── vanna/                     # Vanna相关代码
│   │   ├── __init__.py
│   │   ├── setup.py               # Vanna初始化
│   │   ├── trainer.py             # 训练逻辑
│   │   └── query_processor.py     # 查询处理
│   │
│   ├── schemas/                   # 数据结构定义
│   │   ├── __init__.py
│   │   ├── request.py             # 请求数据结构
│   │   └── response.py            # 响应数据结构
│   │
│   └── utils/                     # 工具函数
│       ├── __init__.py
│       ├── logger.py              # 日志工具
│       └── helpers.py             # 辅助函数
│
├── data/                          # 数据相关
│   ├── schema/                    # 数据库结构定义
│   │   ├── tables.sql             # 表结构定义
│   │   └── relationships.sql      # 关系定义
│   │
│   ├── seed/                      # 示例数据
│   │   └── seed_data.sql          # 数据填充脚本
│   │
│   └── training/                  # Vanna训练数据
│       ├── simple_queries.json    # 简单查询示例
│       ├── filter_queries.json    # 条件过滤查询示例
│       ├── join_queries.json      # 连接查询示例
│       └── complex_queries.json   # 复杂查询示例
│
├── tests/                         # 测试代码
│   ├── __init__.py
│   ├── test_vanna.py              # Vanna功能测试
│   ├── test_langchain.py          # LangChain集成测试
│   └── test_security.py           # 安全性测试
│
├── scripts/                       # 实用脚本
│   ├── setup_db.py                # 数据库设置脚本
│   └── generate_training_data.py  # 训练数据生成脚本
│
├── web/                           # Web界面（可选）
│   ├── __init__.py
│   ├── app.py                     # Web应用入口
│   ├── routes.py                  # 路由定义
│   └── templates/                 # HTML模板
│       ├── index.html
│       └── results.html
│
└── notebooks/                     # Jupyter笔记本
    ├── exploration.ipynb          # 数据探索笔记本
    └── demo.ipynb                 # 演示笔记本