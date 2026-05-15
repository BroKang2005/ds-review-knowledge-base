from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.pages import api_page, ask_page, practice_page, profile_page, summary_page
from backend.schemas import DEFAULT_STUDENT_ID
from backend.services import ReviewService


@st.cache_resource
def get_service() -> ReviewService:
    return ReviewService()


def render_chapter_review(service: ReviewService, student_id: str) -> None:
    st.subheader("章节复习")
    modules = service.list_modules()
    module = st.selectbox("选择章节", modules)
    concepts = service.list_concepts_by_module(module)
    st.markdown("**章节知识点**")
    for concept in concepts[:12]:
        st.write(f"- {concept.get('name')} ({concept.get('id')})")
    target = st.selectbox("选择目标知识点", [item.get("id") for item in concepts] or [""])
    if st.button("生成复习路径", use_container_width=True) and target:
        st.session_state["learning_path"] = service.generate_learning_path(student_id, target)
    path = st.session_state.get("learning_path")
    if path:
        st.markdown("**前置学习路径**")
        for item in path.get("prerequisite_path", []):
            st.write(f"- {item['concept'].get('name')}：{item['status']}")
        st.markdown("**原子知识点步骤**")
        for item in path.get("atomic_steps", []):
            st.write(f"- {item['concept'].get('name')}：{item['status']}")
        st.info(path.get("next_action", ""))


def main() -> None:
    st.set_page_config(page_title="数据结构智能复习助手", layout="wide")
    st.title("数据结构智能复习助手")
    st.caption("基于 JSON 知识库和规则驱动多智能体的期末复习原型")
    try:
        service = get_service()
    except Exception as exc:  # pragma: no cover - UI safety net
        st.error("系统初始化失败，请检查启动目录、知识库 JSON 和依赖环境。")
        st.exception(exc)
        return

    with st.sidebar:
        st.header("学生")
        student_id = st.text_input("学生 ID", value=DEFAULT_STUDENT_ID)
        goal = st.text_input("当前复习目标", value="期末复习数据结构")
        if st.button("保存目标"):
            service.orchestrator.profile_agent.update_goal(student_id, goal)
            st.success("已保存")

    tabs = st.tabs(["知识问答", "章节复习", "做题练习", "学生画像", "复习总结", "API 管理"])
    with tabs[0]:
        ask_page.render(service, student_id)
    with tabs[1]:
        render_chapter_review(service, student_id)
    with tabs[2]:
        practice_page.render(service, student_id)
    with tabs[3]:
        profile_page.render(service, student_id)
    with tabs[4]:
        summary_page.render(service, student_id)
    with tabs[5]:
        api_page.render(service)


if __name__ == "__main__":
    main()
