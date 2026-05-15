# ds-review-knowledge-base

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
