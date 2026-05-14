from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

MODULES = {
    "COMPLEXITY": ("绪论与复杂度分析", ["算法五大特性", "时间复杂度分析", "空间复杂度分析", "递归复杂度", "抽象数据类型"]),
    "LIST": ("线性表", ["顺序表基本操作", "单链表基本操作", "双链表操作", "循环链表", "线性表应用题"]),
    "STACK": ("栈与队列", ["栈的顺序存储", "栈的链式存储", "栈的应用", "队列的顺序存储", "循环队列"]),
    "STRING": ("串、数组与广义表", ["串的基本概念", "KMP模式匹配", "数组存储地址计算", "特殊矩阵压缩存储", "广义表深度与长度"]),
    "TREE": ("树与二叉树", ["二叉树基本性质", "二叉树遍历", "遍历序列还原二叉树", "线索二叉树", "哈夫曼树"]),
    "GRAPH": ("图", ["图的存储结构", "图的DFS遍历", "图的BFS遍历", "最小生成树", "最短路径"]),
    "SEARCH": ("查找", ["顺序查找", "折半查找", "二叉排序树", "平衡二叉树", "哈希表"]),
    "SORT": ("排序", ["插入排序", "交换排序", "选择排序", "归并排序", "排序算法比较"]),
}

ERRORS = [
    ("ERR_COMPLEXITY_001", "时间复杂度循环变量分析错误", ["DS_COMPLEXITY_002"]),
    ("ERR_LIST_001", "链表插入指针顺序错误", ["DS_LIST_002"]),
    ("ERR_LIST_002", "链表删除结点断链", ["DS_LIST_002"]),
    ("ERR_STACK_001", "栈出栈序列判断错误", ["DS_STACK_001"]),
    ("ERR_QUEUE_001", "循环队列判空判满混淆", ["DS_STACK_005"]),
    ("ERR_RECURSION_001", "递归终止条件遗漏", ["DS_COMPLEXITY_004"]),
    ("ERR_TREE_001", "二叉树叶子结点公式使用错误", ["DS_TREE_001"]),
    ("ERR_TREE_002", "二叉树遍历顺序混淆", ["DS_TREE_002"]),
    ("ERR_TREE_003", "遍历序列还原根结点判断错误", ["DS_TREE_003"]),
    ("ERR_TREE_004", "哈夫曼树构造步骤错误", ["DS_TREE_005"]),
    ("ERR_GRAPH_001", "DFS与BFS混淆", ["DS_GRAPH_002", "DS_GRAPH_003"]),
    ("ERR_GRAPH_002", "邻接矩阵和邻接表复杂度混淆", ["DS_GRAPH_001"]),
    ("ERR_GRAPH_003", "Dijkstra更新过程错误", ["DS_GRAPH_005"]),
    ("ERR_GRAPH_004", "Floyd中间顶点更新逻辑错误", ["DS_GRAPH_005"]),
    ("ERR_GRAPH_005", "最小生成树与最短路径混淆", ["DS_GRAPH_004", "DS_GRAPH_005"]),
    ("ERR_SEARCH_001", "折半查找判定树理解错误", ["DS_SEARCH_002"]),
    ("ERR_SEARCH_002", "哈希冲突处理错误", ["DS_SEARCH_005"]),
    ("ERR_SEARCH_003", "平均查找长度计算错误", ["DS_SEARCH_001", "DS_SEARCH_005"]),
    ("ERR_SORT_001", "排序稳定性判断错误", ["DS_SORT_005"]),
    ("ERR_SORT_002", "快速排序最坏复杂度理解错误", ["DS_SORT_002"]),
]

FORMULAS = {
    "COMPLEXITY": ["T(n) 通常保留最高阶项", "O(1) < O(log n) < O(n) < O(n log n) < O(n^2)"],
    "LIST": ["顺序表插入平均移动 n/2 个元素", "单链表查找时间复杂度为 O(n)"],
    "STACK": ["栈遵循后进先出 LIFO", "循环队列长度为 (rear - front + maxsize) % maxsize"],
    "STRING": ["KMP 利用 next 数组避免主串指针回退", "行优先地址按低维下标变化最快计算"],
    "TREE": ["二叉树第 i 层最多有 2^{i-1} 个结点", "任意非空二叉树满足 n0 = n2 + 1"],
    "GRAPH": ["邻接矩阵空间复杂度 O(n^2)", "Dijkstra 每轮选取当前最短的未确定顶点"],
    "SEARCH": ["折半查找要求线性表有序且顺序存储", "装填因子影响哈希表查找效率"],
    "SORT": ["快速排序平均时间复杂度 O(n log n)", "稳定排序不改变相等关键字的相对次序"],
}


def dump(name: str, data: object) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_concepts() -> list[dict]:
    concepts = []
    for prefix, (module, names) in MODULES.items():
        for i, name in enumerate(names, 1):
            cid = f"DS_{prefix}_{i:03d}"
            level = "基础" if i == 1 else "重点" if i in (2, 3) else "难点" if i == 4 else "综合"
            importance = 5 if i in (2, 3, 5) else 4
            prereq = [] if cid == "DS_COMPLEXITY_001" else ([f"DS_{prefix}_{i-1:03d}"] if i > 1 else ["DS_COMPLEXITY_001"])
            concepts.append({
                "id": cid, "name": name, "module": module, "topic": name, "level": level,
                "importance": importance, "exam_frequency": importance, "difficulty": min(5, 1 + i),
                "description": f"掌握{name}的定义、核心操作、复杂度和期末常见考查方式。",
                "prerequisites": prereq, "related_concepts": [], "formulas": FORMULAS[prefix],
                "common_mistakes": ["只记结论不理解适用条件", "忽略边界情况", "混淆相似概念"],
                "question_types": ["选择题", "填空题", "计算题"],
                "learning_suggestion": f"先复习{name}的定义和步骤，再完成典型题巩固边界条件。",
                "mastery_criteria": f"能够独立解释{name}并完成基础题和中等应用题。",
            })
    names = {c["id"]: c["name"] for c in concepts}
    for c in concepts:
        c["related_concepts"] = [names[p] for p in c["prerequisites"] if p in names]
    return concepts


def build_errors() -> list[dict]:
    return [{
        "error_id": eid, "name": name, "related_knowledge": related,
        "error_description": f"学生在处理{name}时，对概念条件、操作顺序或复杂度来源判断不准确。",
        "typical_behavior": ["只套结论", "边界条件处理错误", "题目变形后误判"],
        "diagnosis_rule": f"错题涉及 {', '.join(related)} 且答案体现该问题时触发。",
        "remediation": ["回看核心规则", "完成 3 道基础辨析题", "完成 2 道中等应用题"],
    } for eid, name, related in ERRORS]


def build_questions(concepts: list[dict]) -> list[dict]:
    err_by_concept = {}
    for eid, _, related in ERRORS:
        for cid in related:
            err_by_concept.setdefault(cid, eid)
    questions, qtypes = [], ["选择题", "填空题", "判断题", "计算题", "算法填空题", "综合分析题"]
    for idx, c in enumerate(concepts, 1):
        for variant in range(2):
            qtype = qtypes[(idx + variant) % len(qtypes)]
            if qtype == "选择题":
                stem = f"关于{c['name']}，下列说法较合理的是哪一项？"
                options = ["只需背名称", "需要掌握定义、操作过程和适用条件", "不用分析边界条件", "复杂度与规模无关"]
                answer = options[1]
            elif qtype == "判断题":
                stem, options, answer = f"{c['name']}只需要记忆定义，通常不需要关注边界条件。", ["正确", "错误"], "错误"
            elif qtype == "填空题":
                stem, options, answer = f"{c['name']}所在一级模块是____。", [], c["module"]
            else:
                stem, options, answer = f"请说明{c['name']}的核心解题思路。", [], "先明确结构定义，再写出操作步骤、边界条件和复杂度。"
            questions.append({
                "question_id": f"Q_{c['id']}_{variant + 1:03d}", "question_type": qtype,
                "difficulty": c["difficulty"], "stem": stem, "options": options, "answer": answer,
                "analysis": f"本题考查{c['name']}，需要结合定义、操作步骤、适用条件和常见错因分析。",
                "knowledge_points": [c["id"]], "common_errors": [err_by_concept[c["id"]]] if c["id"] in err_by_concept else [],
                "exam_frequency": c["exam_frequency"], "estimated_time": 2 if c["difficulty"] <= 3 else 4,
                "tags": [c["module"], c["topic"], c["level"]],
            })
    return questions


def build_relations(concepts: list[dict]) -> list[dict]:
    ids = {c["id"] for c in concepts}
    relations = []
    for c in concepts:
        for p in c["prerequisites"]:
            if p in ids:
                relations.append({"source": p, "relation": "prerequisite", "target": c["id"], "description": f"{p} 是 {c['id']} 的前置知识。"})
    explicit = [("DS_LIST_001", "contrast_with", "DS_LIST_002"), ("DS_STACK_003", "used_in", "DS_STACK_003"), ("DS_STACK_005", "used_in", "DS_GRAPH_003"), ("DS_GRAPH_003", "similar_to", "DS_TREE_002"), ("DS_GRAPH_002", "used_in", "DS_GRAPH_001"), ("DS_TREE_002", "frequently_tested_with", "DS_TREE_003"), ("DS_TREE_005", "used_in", "DS_TREE_005"), ("DS_GRAPH_005", "contrast_with", "DS_GRAPH_005"), ("DS_SORT_005", "frequently_tested_with", "DS_SORT_002")]
    for s, r, t in explicit:
        relations.append({"source": s, "relation": r, "target": t, "description": "典型期末复习关联关系。"})
    by_module = {}
    for c in concepts:
        by_module.setdefault(c["module"], []).append(c["id"])
    for mids in by_module.values():
        for a, b in zip(mids, mids[1:]):
            relations.append({"source": a, "relation": "frequently_tested_with", "target": b, "description": "同模块高频共考。"})
        for b in mids[1:]:
            relations.append({"source": mids[0], "relation": "includes", "target": b, "description": "同一模块知识点。"})
    return relations[:70]


def build_learning_paths() -> list[dict]:
    return [
        {"path_id": "PATH_FOUNDATION_REPAIR_DS", "name": "基础补救型复习路径", "target_user": "基础薄弱学生", "sequence": ["复杂度", "线性表", "栈与队列", "树", "查找", "排序"], "strategy": "先补定义和基本操作。", "daily_plan": "每天 1 到 2 个主题。"},
        {"path_id": "PATH_FINAL_REVIEW_DS", "name": "期末冲刺型复习路径", "target_user": "短期系统复习学生", "sequence": ["复杂度分析", "链表", "栈队列", "二叉树", "图", "查找", "排序"], "strategy": "围绕高频考点集中复习。", "daily_plan": "每天 2 个高频模块。"},
        {"path_id": "PATH_HIGH_SCORE_DS", "name": "高分提升型复习路径", "target_user": "冲刺高分学生", "sequence": ["递归", "链表综合", "KMP", "树还原", "图算法", "哈希", "排序比较"], "strategy": "聚焦难点和综合题。", "daily_plan": "每天 1 个难点主题。"},
    ]


def build_student_mastery(concepts: list[dict]) -> list[dict]:
    scores, rows = [0.32, 0.55, 0.76, 0.91], []
    for i, c in enumerate(concepts[:24]):
        score = scores[i % 4]
        status = "not_mastered" if score < 0.4 else "partially_mastered" if score < 0.7 else "basically_mastered" if score < 0.9 else "mastered"
        rows.append({"student_id": "S001", "knowledge_id": c["id"], "mastery_score": score, "attempt_count": 8 + i, "correct_count": int((8 + i) * score), "recent_error_count": max(0, 4 - i % 5), "last_review_time": "2026-05-14", "status": status})
    return rows


def main() -> None:
    concepts = build_concepts()
    dump("concepts.json", concepts)
    dump("errors.json", build_errors())
    dump("questions.json", build_questions(concepts))
    dump("relations.json", build_relations(concepts))
    dump("learning_paths.json", build_learning_paths())
    dump("student_mastery_sample.json", build_student_mastery(concepts))


if __name__ == "__main__":
    main()
