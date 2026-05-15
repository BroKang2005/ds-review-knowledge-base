from __future__ import annotations

import streamlit as st


def render(service, student_id: str) -> None:
    st.subheader("复习总结")
    summary = service.generate_summary(student_id)
    st.metric("近期正确率", summary.get("recent_accuracy", 0.0))
    st.write("错题数量：", summary.get("wrong_question_count", 0))
    st.markdown("**本次/近期复习知识点**")
    for concept in summary.get("reviewed_concepts", []):
        st.write(f"- {concept.get('name')} ({concept.get('id')})")
    st.markdown("**仍需加强**")
    st.write(summary.get("weak_concepts", []) or "暂无")
    st.markdown("**下一步建议**")
    for item in summary.get("next_suggestions", []):
        st.info(item)

