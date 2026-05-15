# ds-review-knowledge-base

# 数据结构智能复习助手

这是一个基于数据结构知识库和规则驱动多智能体协同机制的软件原型，面向高校学生期末复习场景。

## 功能

- 知识点问答与个性化讲解
- 章节复习与学习路径规划
- 题目推荐与做题练习
- 错题诊断与复习建议
- 学生画像更新
- 阶段性复习总结
- Agent API 管理与本地调用日志

## 运行

```bash
pip install -r requirements.txt
python scripts/init_demo_data.py
streamlit run app/streamlit_app.py
```

也可以运行命令行 smoke demo：

```bash
python main.py
```

## 检查知识库

```bash
python scripts/validate_kb.py
python scripts/kb_stats.py
```

## 目录说明

- `app/`: Streamlit 前端页面。
- `backend/`: 服务层和统一 API。
- `backend/agent_api_manager.py`: 智能体 API 注册、调用、校验和日志管理。
- `orchestrator/`: 多智能体调度器。
- `agents/`: 七个规则驱动智能体。
- `knowledge_base/data/`: 已有数据结构知识库 JSON。
- `data/`: 学生画像、答题记录、错题记录和复习 session。
- `scripts/`: 初始化、校验、统计和索引脚本。
- `docs/`: 系统设计、智能体设计和演示流程。
- `tests/`: 软件框架测试。

## Multi-agent Review Prototype

This repository now includes a runnable multi-agent final-review assistant for the data-structure knowledge base.

- `knowledge_base/agents/`: student profile, retrieval, explanation, recommendation, error diagnosis, learning path, and summary agents.
- `knowledge_base/orchestrator/review_orchestrator.py`: coordinates the full workflow.
- `knowledge_base/app/demo_cli.py`: runs a command-line demo from query to diagnosis and summary.

Run the demo:

```bash
cd knowledge_base
python app/demo_cli.py --query DS_TREE_001 --goal 期末复习树结构
```

《数据结构》期末复习知识库原型，包含知识点、题目、错因诊断、学习路径规划和多智能体 Prompt。

## Quick Start

```bash
cd knowledge_base
python tools/build_seed_data.py
python src/demo.py
python -m unittest discover -s tests
```

第一版只使用 Python 标准库，无需安装额外依赖。

## Contents

- `knowledge_base/src/`: 加载、检索、诊断、规划和 demo 代码
- `knowledge_base/tools/build_seed_data.py`: 生成 40 个知识点、80 道题、70 条关系、20 个错因的数据脚本
- `knowledge_base/prompts/`: tutor、diagnosis、planner、question 四类智能体提示词
- `knowledge_base/tests/`: unittest 测试
- `knowledge_base/data/`: 运行数据生成脚本后生成 JSON 文件
