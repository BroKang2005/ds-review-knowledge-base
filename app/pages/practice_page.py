from __future__ import annotations

import streamlit as st


def render(service, student_id: str) -> None:
    st.subheader("做题练习")
    last = st.session_state.get("last_answer", {})
    default_concept = last.get("retrieval", {}).get("primary_concept", {}).get("id")
    concept_id = st.text_input("知识点 ID（可留空按薄弱点推荐）", value=default_concept or "")
    if st.button("刷新推荐题", use_container_width=True):
        st.session_state["practice_questions"] = service.recommend_questions(student_id, concept_id or None)

    questions = st.session_state.get("practice_questions") or last.get("recommendations") or {"recommendations": []}
    recommendations = questions.get("recommendations", [])
    if not recommendations:
        st.write("暂无推荐题，请先在知识问答区输入一个问题。")
        return

    labels = [f"{item['question']['question_id']} - {item['question']['stem'][:40]}" for item in recommendations]
    selected = st.selectbox("选择题目", labels)
    index = labels.index(selected)
    question = recommendations[index]["question"]
    st.markdown(f"**题干：** {question.get('stem')}")
    options = question.get("options", [])
    if options:
        answer = st.radio("选择答案", options)
    else:
        answer = st.text_area("输入答案")

    if st.button("提交答案", use_container_width=True):
        st.session_state["last_diagnosis"] = service.submit_answer(student_id, question["question_id"], answer)

    diagnosis_result = st.session_state.get("last_diagnosis")
    if diagnosis_result:
        diagnosis = diagnosis_result.get("diagnosis", {})
        if diagnosis.get("is_correct"):
            st.success("回答正确")
        else:
            st.error("回答错误")
        st.write("标准答案：", diagnosis.get("standard_answer", ""))
        st.write("解析：", diagnosis.get("analysis", ""))
        for item in diagnosis.get("suggestion", []):
            st.info(item)

