from __future__ import annotations

import streamlit as st


def render(service, student_id: str) -> None:
    st.subheader("学生画像")
    profile = service.get_profile(student_id)
    col1, col2, col3 = st.columns(3)
    col1.metric("答题数量", profile.get("answer_count", 0))
    col2.metric("错题数量", profile.get("wrong_question_count", 0))
    col3.metric("近期正确率", profile.get("recent_accuracy", 0.0))

    st.markdown("**已学习知识点**")
    st.write(profile.get("learned_concepts", []) or "暂无")
    st.markdown("**已掌握知识点**")
    st.write(profile.get("mastered_concepts", []) or "暂无")
    st.markdown("**薄弱知识点**")
    st.write(profile.get("weak_concepts", []) or "暂无")

