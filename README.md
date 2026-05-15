# 数据结构智能复习助手

本仓库是一个面向高校学生期末复习场景的“数据结构智能复习助手”软件原型。项目在已有《数据结构》知识库基础上，加入多智能体协同框架，用于完成知识点问答、个性化讲解、题目推荐、错题诊断、学习路径规划、学生画像更新和阶段性复习总结。

当前版本以可运行、流程完整、结构清晰为目标，主要采用 Python、Streamlit、JSON 数据存储和规则驱动 Agent 实现，后续可以继续接入大模型 API 与更复杂的检索推理能力。

## 核心能力

- 知识点问答：根据学生输入的问题检索相关概念、原子知识点、关系和题目。
- 个性化讲解：结合学生薄弱点生成定义、考点、示例、易错点和小结。
- 题目推荐：按知识点、薄弱项和难度分层推荐练习，减少重复推荐。
- 错题诊断：判断学生答案正误，返回标准答案、解析、错误类型和复习建议。
- 学生画像：记录已学知识点、错题、答题历史、薄弱知识点和当前复习目标。
- 学习路径：基于 prerequisite、contains、confuses_with 等关系生成复习顺序。
- 复习总结：汇总本次学习、答题、错题和下一步建议。
- Agent API 管理：统一注册、调用、校验和记录各智能体接口，便于后续替换为真实 API 或 LLM 调用。

## 项目结构

```text
.
├── app/                         # Streamlit 前端页面
├── agents/                      # 七个规则驱动智能体
├── backend/                     # 服务层、API 封装和 Agent API 管理器
├── orchestrator/                # ReviewOrchestrator 多智能体调度器
├── knowledge_base/              # 已有数据结构知识库与早期原型
│   └── data/                    # concepts、questions、relations、errors 等 JSON 数据
├── data/                        # 学生画像、答题记录、错题记录、复习 session 和 API 调用日志
├── scripts/                     # 初始化、校验、统计和索引脚本
├── docs/                        # 系统设计、智能体设计和演示流程文档
└── tests/                       # 单元测试
```

## 快速启动

安装依赖：

```bash
pip install -r requirements.txt
```

初始化演示学生数据：

```bash
python scripts/init_demo_data.py
```

启动 Streamlit 页面：

```bash
streamlit run app/streamlit_app.py
```

如果本机 8501 端口被占用，也可以使用仓库提供的 PowerShell 启动脚本：

```powershell
powershell -ExecutionPolicy Bypass -File .\run_streamlit.ps1
```

命令行 smoke demo：

```bash
python main.py
```

## 知识库检查

```bash
python scripts/validate_kb.py
python scripts/kb_stats.py
```

## 测试

```bash
python -m unittest discover -s tests
```

## 当前演示流程

1. 选择演示学生 `demo_student`。
2. 在知识问答区输入问题，例如“Dijkstra 算法怎么理解？”。
3. 系统检索知识库并返回讲解、相关知识点和推荐题目。
4. 在做题练习区提交答案。
5. 系统进行正误判断、错因分析并更新学生画像。
6. 在学生画像区查看薄弱知识点、错题数量和近期正确率。
7. 在复习总结区生成本次复习总结和下一步建议。

## 早期知识库原型

`knowledge_base/` 目录中保留了早期数据结构知识库原型，包括知识点、题目、错因诊断、学习路径规划和多智能体 Prompt。可以单独运行：

```bash
cd knowledge_base
python tools/build_seed_data.py
python src/demo.py
python -m unittest discover -s tests
```
