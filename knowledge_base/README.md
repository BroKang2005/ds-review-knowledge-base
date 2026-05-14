# 数据结构期末复习知识库

这是一个轻量级《数据结构》期末复习知识库原型，面向“多智能体协同的高校学生学科期末复习软件”。项目提供结构化知识点、题目、错因、知识关系、学习路径，以及基础的加载、检索、诊断和复习计划生成接口。

最近更新：2026-05-15

## 目录结构

```text
knowledge_base/
├── data/
│   ├── concepts.json
│   ├── relations.json
│   ├── questions.json
│   ├── errors.json
│   ├── learning_paths.json
│   └── student_mastery_sample.json
├── prompts/
│   ├── tutor_agent.md
│   ├── diagnosis_agent.md
│   ├── planner_agent.md
│   └── question_agent.md
├── src/
│   ├── kb_loader.py
│   ├── kb_search.py
│   ├── diagnosis.py
│   ├── planner.py
│   └── demo.py
├── tests/
├── tools/
│   └── build_seed_data.py
├── README.md
└── requirements.txt
```

## 数据文件说明

- `concepts.json`：数据结构知识点，覆盖复杂度、线性表、栈与队列、串与数组、树、图、查找、排序 8 个模块；采用“模块 -> 主题 -> 知识点 -> 原子知识点”四级结构。
- `relations.json`：知识点之间的 parent_child、前置、对比、应用、错因关联和高频共考关系，已清理自环、重复和过泛关系。
- `questions.json`：期末复习题目，每题至少映射到一个 atomic 粒度知识点。
- `errors.json`：常见错因库，每个错因至少关联一个 atomic 粒度知识点，用于错题诊断和补救建议。
- `learning_paths.json`：基础补救、期末冲刺和高分提升三类学习路径。
- `student_mastery_sample.json`：模拟学生掌握度数据。

## 安装依赖

第一版只使用 Python 标准库：

```bash
pip install -r requirements.txt
```

## 生成数据

如需重新生成种子数据：

```bash
python tools/build_seed_data.py
```

## 运行 Demo

```bash
python src/demo.py
```

Demo 会依次展示：

1. 加载并校验知识库
2. 搜索“二叉树”
3. 查询相关题目
4. 模拟学生做错循环队列题
5. 根据错题定位到原子知识点并输出错因诊断
6. 生成 7 天复习计划

## 样例输出

```text
=== 知识库规模 ===
{
  "concepts": 208,
  "atomic_concepts": 132,
  "questions": 483,
  "relations": 708,
  "errors": 71
}
```

## 后续扩展方向

- 增加更细粒度的题目难度和考点标签。
- 接入 TF-IDF 或向量检索，实现语义搜索。
- 增加学生掌握度更新算法。
- 提供 FastAPI 接口，供前端和智能体调用。
- 增加知识图谱可视化页面。
