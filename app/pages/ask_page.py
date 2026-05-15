from __future__ import annotations

import streamlit as st


def render(service, student_id: str) -> None:
    st.subheader("知识问答")
    query = st.text_input("输入数据结构相关问题", value="Dijkstra 算法怎么理解？")
    if st.button("生成讲解", use_container_width=True):
        st.session_state["last_answer"] = service.answer_question(student_id, query)

    result = st.session_state.get("last_answer")
    if not result:
        return

    concept = result["retrieval"].get("primary_concept", {})
    explanation = result.get("explanation", {})
    st.markdown(f"**命中知识点：** {concept.get('name', '未命中')}")
    st.write(explanation.get("definition", ""))
    st.markdown("**考点提示**")
    for item in explanation.get("exam_focus", []):
        st.write(f"- {item}")
    st.markdown("**易错提醒**")
    for item in explanation.get("common_mistakes", []):
        st.warning(item)

    st.markdown("**相关题目推荐**")
    for item in result.get("recommendations", {}).get("recommendations", []):
        question = item["question"]
        st.info(f"{item['order']}. {question.get('stem')} ({item.get('reason')})")

