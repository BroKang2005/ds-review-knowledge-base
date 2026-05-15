# 智能体设计

- `StudentProfileAgent`：维护学生画像、答题历史、错题和正确率。
- `KnowledgeRetrievalAgent`：从 JSON 知识库检索概念、原子知识点、题目、前置知识和易混知识。
- `ExplanationAgent`：生成知识点讲解、考点提示、示例和易错提醒。
- `QuestionRecommendationAgent`：根据目标知识点和薄弱点推荐题目，并避免重复推荐。
- `ErrorDiagnosisAgent`：判断答案正误，返回标准答案、解析、错因和建议。
- `LearningPathAgent`：根据 prerequisite 和层级结构生成复习路径。
- `SummaryAgent`：汇总近期复习、错题、薄弱点和下一步计划。

各 Agent 只接收和返回 dict，便于后续替换实现。

## API 管理模块

`backend/agent_api_manager.py` 提供统一 Agent API 注册与调用入口。

当前内置 endpoint：

- `student_profile.get`
- `student_profile.update_goal`
- `knowledge.retrieve`
- `knowledge.get_concept`
- `explanation.explain`
- `question.recommend`
- `error.diagnose`
- `learning_path.plan`
- `summary.generate`

每次调用返回统一 envelope：

```json
{
  "ok": true,
  "endpoint": "knowledge.retrieve",
  "timestamp": "...",
  "data": {},
  "error": ""
}
```

调用日志写入 `data/agent_api_calls.json`，后续可扩展鉴权、限流、远程 API、LLM provider 配置与成本统计。
