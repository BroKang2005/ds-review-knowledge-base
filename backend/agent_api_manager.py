from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from agents.schemas import now_iso
from backend.services import write_json


AgentCallable = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class AgentEndpoint:
    name: str
    agent: str
    action: str
    handler: AgentCallable
    required_fields: tuple[str, ...] = ()
    description: str = ""


class AgentAPIManager:
    """Central registry and invocation manager for all agent APIs.

    The manager gives the app one stable place to call agents from. It is
    intentionally local and rule-driven now, but the same interface can later
    dispatch to FastAPI, LLM tools, remote services, or async workers.
    """

    def __init__(self, orchestrator: Any, log_path: str | None = None):
        self.orchestrator = orchestrator
        self.log_path = log_path
        self.endpoints: dict[str, AgentEndpoint] = {}
        self._register_defaults()

    def list_endpoints(self) -> list[dict[str, Any]]:
        return [
            {
                "name": endpoint.name,
                "agent": endpoint.agent,
                "action": endpoint.action,
                "required_fields": list(endpoint.required_fields),
                "description": endpoint.description,
            }
            for endpoint in self.endpoints.values()
        ]

    def call(self, endpoint_name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = payload or {}
        endpoint = self.endpoints.get(endpoint_name)
        if not endpoint:
            return self._envelope(endpoint_name, False, None, f"Unknown agent endpoint: {endpoint_name}")

        missing = [field for field in endpoint.required_fields if field not in payload or payload[field] in (None, "")]
        if missing:
            return self._envelope(endpoint_name, False, None, f"Missing required fields: {', '.join(missing)}")

        try:
            data = endpoint.handler(**payload)
            response = self._envelope(endpoint_name, True, data, "")
        except Exception as exc:  # pragma: no cover - defensive boundary
            response = self._envelope(endpoint_name, False, None, str(exc))
        self._log_call(endpoint_name, payload, response)
        return response

    def call_many(self, calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.call(item.get("endpoint", ""), item.get("payload", {})) for item in calls]

    def register(self, endpoint: AgentEndpoint) -> None:
        self.endpoints[endpoint.name] = endpoint

    def _register_defaults(self) -> None:
        o = self.orchestrator
        self.register(
            AgentEndpoint(
                name="student_profile.get",
                agent="StudentProfileAgent",
                action="get_profile_summary",
                required_fields=("student_id",),
                description="获取学生画像摘要。",
                handler=lambda student_id: o.profile_agent.summarize(student_id),
            )
        )
        self.register(
            AgentEndpoint(
                name="student_profile.update_goal",
                agent="StudentProfileAgent",
                action="update_goal",
                required_fields=("student_id", "goal"),
                description="更新学生当前复习目标。",
                handler=lambda student_id, goal: o.profile_agent.update_goal(student_id, goal),
            )
        )
        self.register(
            AgentEndpoint(
                name="knowledge.retrieve",
                agent="KnowledgeRetrievalAgent",
                action="retrieve",
                required_fields=("query",),
                description="按关键词或知识点 ID 检索知识库。",
                handler=lambda query: o.retrieval_agent.retrieve(query),
            )
        )
        self.register(
            AgentEndpoint(
                name="knowledge.get_concept",
                agent="KnowledgeRetrievalAgent",
                action="get_concept",
                required_fields=("concept_id",),
                description="按 concept_id 获取知识点。",
                handler=lambda concept_id: o.retrieval_agent.get_concept(concept_id),
            )
        )
        self.register(
            AgentEndpoint(
                name="explanation.explain",
                agent="ExplanationAgent",
                action="explain",
                required_fields=("student_id", "concept_id"),
                description="生成面向学生的知识点讲解。",
                handler=lambda student_id, concept_id: o.explanation_agent.explain(
                    o.retrieval_agent.get_concept(concept_id),
                    o.profile_agent.summarize(student_id),
                ),
            )
        )
        self.register(
            AgentEndpoint(
                name="question.recommend",
                agent="QuestionRecommendationAgent",
                action="recommend",
                required_fields=("student_id",),
                description="根据知识点或薄弱点推荐题目。",
                handler=lambda student_id, concept_id=None, limit=5: o.question_agent.recommend(
                    o.profile_agent.get_profile(student_id),
                    concept_id=concept_id,
                    limit=int(limit),
                ),
            )
        )
        self.register(
            AgentEndpoint(
                name="error.diagnose",
                agent="ErrorDiagnosisAgent",
                action="diagnose",
                required_fields=("question_id", "student_answer"),
                description="判断答案并输出错因诊断。",
                handler=lambda question_id, student_answer: o.error_agent.diagnose(
                    o.retrieval_agent.get_question(question_id),
                    student_answer,
                ),
            )
        )
        self.register(
            AgentEndpoint(
                name="learning_path.plan",
                agent="LearningPathAgent",
                action="plan",
                required_fields=("student_id", "target_concept_id"),
                description="生成个性化学习路径。",
                handler=lambda student_id, target_concept_id: o.learning_path_agent.plan(
                    o.profile_agent.summarize(student_id),
                    target_concept_id,
                ),
            )
        )
        self.register(
            AgentEndpoint(
                name="summary.generate",
                agent="SummaryAgent",
                action="summarize",
                required_fields=("student_id",),
                description="生成阶段性复习总结。",
                handler=lambda student_id: o.summary_agent.summarize(
                    o.profile_agent.summarize(student_id),
                    o.profile_agent.get_sessions(student_id),
                ),
            )
        )

    def _envelope(self, endpoint_name: str, ok: bool, data: Any, error: str) -> dict[str, Any]:
        return {
            "ok": ok,
            "endpoint": endpoint_name,
            "timestamp": now_iso(),
            "data": data,
            "error": error,
        }

    def _log_call(self, endpoint_name: str, payload: dict[str, Any], response: dict[str, Any]) -> None:
        if not self.log_path:
            return
        from backend.services import load_json

        logs = load_json(self.log_path, [])
        logs.append(
            {
                "timestamp": response["timestamp"],
                "endpoint": endpoint_name,
                "payload_keys": sorted(payload.keys()),
                "ok": response["ok"],
                "error": response["error"],
            }
        )
        write_json(self.log_path, logs)

