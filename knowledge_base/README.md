# 数据结构期末复习知识库

这是一个轻量级《数据结构》期末复习知识库原型，面向“多智能体协同的高校学生学科期末复习软件”。项目提供结构化知识点、题目、错因、知识关系、学习路径，以及基础的加载、检索、诊断和复习计划生成接口。

## 安装与运行

```bash
python tools/build_seed_data.py
python src/demo.py
python -m unittest discover -s tests
```

第一版只使用 Python 标准库。

## 数据文件

运行 `python tools/build_seed_data.py` 后会生成：

- `data/concepts.json`
- `data/relations.json`
- `data/questions.json`
- `data/errors.json`
- `data/learning_paths.json`
- `data/student_mastery_sample.json`

## 能力

- 知识点加载与一致性校验
- 关键词检索、模块筛选、难度筛选
- 按知识点查询题目、前置知识和关系
- 根据错题记录进行错因诊断
- 根据薄弱点生成复习计划

## 数据规模

生成后包含 40 个知识点、80 道题、70 条关系、20 个错因和 3 条学习路径。
