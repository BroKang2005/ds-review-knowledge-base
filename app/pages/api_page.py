from __future__ import annotations

import json

import streamlit as st


def render(service) -> None:
    st.subheader("Agent API 管理")
    endpoints = service.list_agent_apis()
    st.caption("统一查看和调试各智能体的本地 API endpoint。")
    st.dataframe(endpoints, use_container_width=True)

    names = [item["name"] for item in endpoints]
    selected = st.selectbox("选择 endpoint", names)
    default_payload = _default_payload(selected)
    payload_text = st.text_area("请求 payload(JSON)", value=json.dumps(default_payload, ensure_ascii=False, indent=2), height=180)

    if st.button("调用 API", use_container_width=True):
        try:
            payload = json.loads(payload_text or "{}")
        except json.JSONDecodeError as exc:
            st.error(f"JSON 格式错误：{exc}")
            return
        response = service.call_agent_api(selected, payload)
        if response.get("ok"):
            st.success("调用成功")
        else:
            st.error(response.get("error", "调用失败"))
        st.json(response)


def _default_payload(endpoint: str) -> dict:
    samples = {
        "student_profile.get": {"student_id": "demo_student"},
        "student_profile.update_goal": {"student_id": "demo_student", "goal": "期末复习图算法"},
        "knowledge.retrieve": {"query": "Dijkstra 算法"},
        "knowledge.get_concept": {"concept_id": "DS_GRAPH_005"},
        "explanation.explain": {"student_id": "demo_student", "concept_id": "DS_GRAPH_005"},
        "question.recommend": {"student_id": "demo_student", "concept_id": "DS_GRAPH_005", "limit": 3},
        "error.diagnose": {"question_id": "Q_DS_GRAPH_005_A01_003", "student_answer": "只需背诵名称即可"},
        "learning_path.plan": {"student_id": "demo_student", "target_concept_id": "DS_GRAPH_005"},
        "summary.generate": {"student_id": "demo_student"},
    }
    return samples.get(endpoint, {})

