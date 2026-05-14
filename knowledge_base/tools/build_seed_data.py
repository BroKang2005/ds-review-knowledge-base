from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


MODULES = [
    (
        "COMPLEXITY",
        "绪论与复杂度分析",
        [
            ("算法五大特性", "算法基础", "基础", 4, 2, "理解有穷性、确定性、可行性、输入和输出。"),
            ("时间复杂度分析", "复杂度分析", "重点", 5, 3, "掌握基本语句、循环和嵌套循环的增长阶估计。"),
            ("空间复杂度分析", "复杂度分析", "重点", 4, 3, "能分析辅助变量、递归栈和额外数组带来的空间消耗。"),
            ("递归复杂度", "递归算法", "难点", 5, 4, "能用递推式或递归树估计递归算法的时间与空间复杂度。"),
            ("抽象数据类型", "数据结构基础", "基础", 3, 2, "理解数据逻辑结构、存储结构和运算集合之间的关系。"),
        ],
    ),
    (
        "LIST",
        "线性表",
        [
            ("顺序表基本操作", "顺序存储", "重点", 5, 2, "掌握顺序表查找、插入、删除的过程和复杂度。"),
            ("单链表基本操作", "链式存储", "重点", 5, 3, "掌握单链表建表、查找、插入和删除的指针变化。"),
            ("双链表操作", "链式存储", "重点", 4, 3, "理解双链表前驱、后继指针的维护顺序。"),
            ("循环链表", "链式存储", "重点", 4, 3, "理解循环链表尾结点与头结点的关系及遍历终止条件。"),
            ("线性表应用题", "综合应用", "综合", 5, 4, "能用顺序表或链表解决合并、逆置、去重等问题。"),
        ],
    ),
    (
        "STACK",
        "栈与队列",
        [
            ("栈的顺序存储", "栈", "重点", 5, 2, "掌握栈顶指针变化、入栈出栈条件和溢出判断。"),
            ("栈的链式存储", "栈", "基础", 3, 2, "理解链栈的头插入与头删除实现。"),
            ("栈的应用", "栈", "重点", 5, 3, "掌握括号匹配、表达式求值和递归模拟。"),
            ("队列的顺序存储", "队列", "重点", 4, 2, "理解队头、队尾指针的移动规则。"),
            ("循环队列", "队列", "重点", 5, 3, "掌握循环队列判空、判满和长度计算。"),
        ],
    ),
    (
        "STRING",
        "串、数组与广义表",
        [
            ("串的基本概念", "串", "基础", 3, 2, "理解串、子串、主串、模式串和位置的定义。"),
            ("KMP模式匹配", "串", "难点", 5, 4, "掌握 next 数组含义及利用失配信息减少比较。"),
            ("数组存储地址计算", "数组", "重点", 5, 3, "能按行优先或列优先计算多维数组元素地址。"),
            ("特殊矩阵压缩存储", "数组", "重点", 4, 4, "掌握对称矩阵、三角矩阵和稀疏矩阵压缩思路。"),
            ("广义表深度与长度", "广义表", "基础", 3, 3, "能计算广义表的长度、深度并理解表头表尾。"),
        ],
    ),
    (
        "TREE",
        "树与二叉树",
        [
            ("二叉树基本性质", "二叉树基础", "重点", 5, 2, "掌握结点数、层数、叶子结点与度为2结点之间的关系。"),
            ("二叉树遍历", "二叉树遍历", "重点", 5, 3, "掌握先序、中序、后序和层序遍历规则。"),
            ("遍历序列还原二叉树", "二叉树遍历", "难点", 5, 4, "能由先序中序或后序中序唯一还原二叉树。"),
            ("线索二叉树", "二叉树进阶", "重点", 4, 4, "理解线索化后空指针域保存前驱和后继。"),
            ("哈夫曼树", "树的应用", "重点", 5, 3, "掌握最优二叉树构造和哈夫曼编码。"),
        ],
    ),
    (
        "GRAPH",
        "图",
        [
            ("图的存储结构", "图基础", "重点", 5, 3, "掌握邻接矩阵、邻接表及其空间复杂度。"),
            ("图的DFS遍历", "图遍历", "重点", 5, 3, "理解深度优先搜索及其连通性判断。"),
            ("图的BFS遍历", "图遍历", "重点", 5, 3, "理解广度优先搜索及其最短层次性质。"),
            ("最小生成树", "图应用", "重点", 5, 4, "掌握 Prim 和 Kruskal 算法的选择规则。"),
            ("最短路径", "图应用", "难点", 5, 4, "掌握 Dijkstra 和 Floyd 的适用条件与更新过程。"),
        ],
    ),
    (
        "SEARCH",
        "查找",
        [
            ("顺序查找", "线性查找", "基础", 3, 2, "理解顺序查找的比较过程和平均查找长度。"),
            ("折半查找", "有序表查找", "重点", 5, 3, "掌握折半查找判定树和查找次数分析。"),
            ("二叉排序树", "树表查找", "重点", 5, 3, "掌握二叉排序树插入、删除和查找过程。"),
            ("平衡二叉树", "树表查找", "难点", 4, 4, "理解 AVL 树失衡类型和旋转调整。"),
            ("哈希表", "散列表", "重点", 5, 4, "掌握散列函数、冲突处理和平均查找长度。"),
        ],
    ),
    (
        "SORT",
        "排序",
        [
            ("插入排序", "插入类排序", "重点", 4, 2, "掌握直接插入排序和希尔排序的过程。"),
            ("交换排序", "交换类排序", "重点", 5, 3, "掌握冒泡排序和快速排序的划分过程。"),
            ("选择排序", "选择类排序", "重点", 4, 2, "掌握简单选择排序和堆排序的特点。"),
            ("归并排序", "归并类排序", "重点", 5, 3, "理解二路归并排序的分治过程和空间代价。"),
            ("排序算法比较", "排序综合", "综合", 5, 4, "比较常见排序算法的复杂度、稳定性和适用场景。"),
        ],
    ),
]


ERROR_SPECS = [
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


ERROR_QUOTAS = {
    "绪论与复杂度分析": ("COMPLEXITY", 6),
    "线性表": ("LIST", 8),
    "栈与队列": ("STACK", 8),
    "串、数组与广义表": ("STRING", 6),
    "树与二叉树": ("TREE", 12),
    "图": ("GRAPH", 12),
    "查找": ("SEARCH", 8),
    "排序": ("SORT", 10),
}


ERROR_PATTERNS = [
    ("适用条件误判", "没有先判断该知识点的前提条件，直接套用结论。"),
    ("边界情况遗漏", "忽略空结构、单元素、首尾位置或临界规模。"),
    ("操作步骤顺序错误", "能说出大致思路，但关键步骤先后顺序不正确。"),
    ("复杂度来源判断错误", "只记复杂度结论，不能解释基本操作执行次数。"),
    ("概念混淆", "把相似概念、相似算法或相似结构的规则混用。"),
    ("题意映射错误", "不能把题目条件准确映射到对应原子知识点。"),
    ("过程跟踪错误", "手算或执行算法时，中间状态记录不完整。"),
    ("结论适用范围扩大", "把只在特定条件下成立的结论当作普遍规律。"),
]


SUPPLEMENTAL_ERROR_ATOMICS = [
    ("ERR_STACK_009", "循环队列队满条件判定混淆", "DS_STACK_005_A02", "把队空条件 front == rear 误当作队满条件，或忘记牺牲一个存储单元的判满公式。"),
]


ATOMIC_OVERRIDES = {
    "DS_STACK_005": [
        ("循环队列队空条件", "判断 front == rear 表示循环队列为空。"),
        ("循环队列队满条件", "掌握牺牲一个存储单元时 (rear + 1) % maxsize == front 表示队满。"),
        ("循环队列长度计算", "能用 (rear - front + maxsize) % maxsize 计算当前元素个数。"),
        ("循环队列入队出队指针变化", "能分别说明入队移动 rear、出队移动 front 的取模更新过程。"),
    ],
    "DS_LIST_002": [
        ("单链表按序查找", "能从头结点或首元结点开始按 next 指针定位目标结点。"),
        ("单链表插入指针顺序", "能正确写出先连新结点后断旧链的插入语句顺序。"),
        ("单链表删除前驱定位", "能先找到被删结点前驱，再修改前驱 next。"),
        ("头插法与尾插法建表", "能区分头插法逆序、尾插法保序的建表特点。"),
    ],
    "DS_TREE_001": [
        ("二叉树第 i 层最大结点数", "能使用第 i 层最多 2^(i-1) 个结点的性质。"),
        ("深度为 k 的二叉树最大结点数", "能使用深度为 k 时最多 2^k - 1 个结点的性质。"),
        ("叶子结点与度为 2 结点关系", "能说明任意非空二叉树 n0 = n2 + 1。"),
        ("完全二叉树编号性质", "能根据编号判断父结点、左孩子和右孩子位置。"),
    ],
    "DS_TREE_002": [
        ("先序遍历规则", "能按根、左、右顺序输出二叉树结点。"),
        ("中序遍历规则", "能按左、根、右顺序输出二叉树结点。"),
        ("后序遍历规则", "能按左、右、根顺序输出二叉树结点。"),
        ("层序遍历规则", "能借助队列按层从左到右访问二叉树。"),
    ],
    "DS_TREE_003": [
        ("先序中序还原二叉树", "能由先序首元素确定根，并在中序中划分左右子树。"),
        ("后序中序还原二叉树", "能由后序末元素确定根，并在中序中划分左右子树。"),
        ("遍历还原唯一性条件", "能判断必须包含中序序列才通常能唯一还原二叉树。"),
        ("还原过程递归划分", "能在左右子树中递归重复定位根结点。"),
    ],
    "DS_GRAPH_002": [
        ("DFS 访问规则", "能说明 DFS 沿未访问邻接点不断深入的访问方式。"),
        ("DFS 递归与栈思想", "能解释 DFS 可用递归或栈实现。"),
        ("DFS 连通性判断", "能用一次 DFS 访问顶点数判断无向图连通性。"),
        ("DFS 生成树", "能识别 DFS 遍历过程中形成的生成树边。"),
    ],
    "DS_GRAPH_003": [
        ("BFS 访问规则", "能说明 BFS 按距离层次逐层扩展顶点。"),
        ("BFS 队列实现", "能解释 BFS 入队、出队和访问标记的顺序。"),
        ("BFS 最短层次性质", "能判断无权图中 BFS 首次到达对应最少边数路径。"),
        ("BFS 与层序遍历关系", "能说明 BFS 与二叉树层序遍历的共同队列思想。"),
    ],
    "DS_GRAPH_004": [
        ("Prim 算法选边规则", "能从已选顶点集合到未选顶点集合中选择最小边。"),
        ("Kruskal 算法选边规则", "能按边权从小到大选取不构成回路的边。"),
        ("最小生成树适用条件", "能说明 MST 面向连通无向带权图。"),
        ("MST 与最短路径区别", "能区分总权值最小的生成树和源点到各点最短路径。"),
    ],
    "DS_GRAPH_005": [
        ("Dijkstra 适用条件", "能判断 Dijkstra 适用于非负权单源最短路径。"),
        ("Dijkstra 松弛更新", "能根据新中间顶点更新 dist 数组。"),
        ("Floyd 中间顶点更新", "能使用 dist[i][k] + dist[k][j] 更新任意两点最短路径。"),
        ("Dijkstra 与 Floyd 对比", "能区分单源最短路径和多源最短路径算法。"),
    ],
    "DS_SEARCH_002": [
        ("折半查找前提条件", "能判断折半查找要求有序且顺序存储。"),
        ("折半查找 mid 计算", "能根据 low、high 计算 mid 并更新查找区间。"),
        ("折半查找判定树", "能根据有序表长度画出或分析判定树。"),
        ("折半查找比较次数", "能估计成功或失败查找的比较次数。"),
    ],
    "DS_SEARCH_005": [
        ("哈希函数构造", "能说明常见散列函数设计目标是均匀分布。"),
        ("线性探测处理冲突", "能按线性探测序列处理哈希冲突。"),
        ("链地址法处理冲突", "能说明同义词结点挂入同一散列地址链表。"),
        ("哈希表平均查找长度", "能根据查找路径计算成功或失败 ASL。"),
    ],
    "DS_SORT_005": [
        ("排序时间复杂度比较", "能比较常见排序算法最好、平均、最坏时间复杂度。"),
        ("排序空间复杂度比较", "能比较原地排序与需要辅助数组的排序。"),
        ("排序稳定性判断", "能判断相等关键字相对次序是否保持。"),
        ("排序适用场景选择", "能根据规模、有序性和稳定性要求选择排序算法。"),
    ],
}


def dump(name: str, data: object) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_concepts() -> list[dict]:
    concepts: list[dict] = []
    for prefix, module, items in MODULES:
        module_id = f"DS_{prefix}_MODULE"
        concepts.append(
            {
                "id": module_id,
                "parent_id": "",
                "granularity": "module",
                "name": module,
                "module": module,
                "topic": module,
                "level": "模块",
                "importance": max(item[3] for item in items),
                "exam_frequency": max(item[3] for item in items),
                "difficulty": max(item[4] for item in items),
                "diagnosable": False,
                "practice_priority": 3,
                "description": f"{module}一级模块，用于组织本模块下的主题、知识点和原子知识点。",
                "prerequisites": [],
                "related_concepts": [],
                "formulas": [],
                "common_mistakes": [],
                "question_types": [],
                "learning_suggestion": f"按主题顺序复习{module}，再进入原子知识点练习。",
                "mastery_criteria": f"能够说明{module}模块的核心主题和高频考点分布。",
            }
        )
        topic_ids: dict[str, str] = {}
        for index, (name, topic, level, importance, difficulty, desc) in enumerate(items, start=1):
            if topic not in topic_ids:
                topic_id = f"DS_{prefix}_TOPIC_{len(topic_ids) + 1:02d}"
                topic_ids[topic] = topic_id
                concepts.append(
                    {
                        "id": topic_id,
                        "parent_id": module_id,
                        "granularity": "topic",
                        "name": topic,
                        "module": module,
                        "topic": topic,
                        "level": "主题",
                        "importance": importance,
                        "exam_frequency": importance,
                        "difficulty": difficulty,
                        "diagnosable": False,
                        "practice_priority": 3,
                        "description": f"{topic}二级主题，用于聚合相关知识点。",
                        "prerequisites": [module_id],
                        "related_concepts": [module],
                        "formulas": [],
                        "common_mistakes": [],
                        "question_types": [],
                        "learning_suggestion": f"先建立{topic}的整体框架，再拆解为可练习的原子知识点。",
                        "mastery_criteria": f"能够列出{topic}下的主要知识点并说明学习顺序。",
                    }
                )
            cid = f"DS_{prefix}_{index:03d}"
            prereq = [topic_ids[topic]]
            if index > 1:
                prereq.append(f"DS_{prefix}_{index - 1:03d}")
            concepts.append(
                {
                    "id": cid,
                    "parent_id": topic_ids[topic],
                    "granularity": "concept",
                    "name": name,
                    "module": module,
                    "topic": topic,
                    "level": level,
                    "importance": importance,
                    "exam_frequency": importance,
                    "difficulty": difficulty,
                    "diagnosable": False,
                    "practice_priority": priority_for(importance, difficulty),
                    "description": desc,
                    "prerequisites": prereq,
                    "related_concepts": [],
                    "formulas": formula_for(prefix, index),
                    "common_mistakes": mistakes_for(cid),
                    "question_types": ["选择题", "填空题", "计算题"],
                    "learning_suggestion": f"先复习{name}的定义和操作过程，再配合典型例题巩固边界条件。",
                    "mastery_criteria": f"能够独立解释{name}，完成相关基础题和中等难度应用题。",
                }
            )
            for atomic_index, (atomic_name, atomic_desc) in enumerate(atomic_specs_for(cid, name, desc), start=1):
                aid = f"{cid}_A{atomic_index:02d}"
                concepts.append(
                    {
                        "id": aid,
                        "parent_id": cid,
                        "granularity": "atomic",
                        "name": atomic_name,
                        "module": module,
                        "topic": topic,
                        "level": level,
                        "importance": importance,
                        "exam_frequency": importance,
                        "difficulty": difficulty,
                        "diagnosable": True,
                        "practice_priority": priority_for(importance, difficulty),
                        "description": atomic_desc,
                        "prerequisites": [cid] if atomic_index == 1 else [cid, f"{cid}_A{atomic_index - 1:02d}"],
                        "related_concepts": [name],
                        "formulas": formula_for(prefix, index),
                        "common_mistakes": mistakes_for(cid),
                        "question_types": ["选择题", "填空题", "计算题"],
                        "learning_suggestion": f"围绕“{atomic_name}”单独完成概念辨析、过程推演和错因复盘。",
                        "mastery_criteria": f"学生能够独立回答“{atomic_name}”相关题目，并能解释适用条件、操作步骤和常见错误。",
                    }
                )
    name_by_id = {c["id"]: c["name"] for c in concepts}
    for concept in concepts:
        related = [name_by_id[p] for p in concept["prerequisites"] if p in name_by_id]
        concept["related_concepts"] = related[:3]
    return concepts


def atomic_specs_for(concept_id: str, concept_name: str, description: str) -> list[tuple[str, str]]:
    if concept_id in ATOMIC_OVERRIDES:
        return ATOMIC_OVERRIDES[concept_id]
    return [
        (f"{concept_name}定义与适用条件", f"能说明{concept_name}的核心定义、适用条件和边界情况。"),
        (f"{concept_name}操作过程与复杂度", f"能根据题目要求推演{concept_name}的操作过程，并分析复杂度。{description}"),
        (f"{concept_name}典型题型识别", f"能从题干条件识别{concept_name}对应的常见考法和易错点。"),
    ]


def priority_for(importance: int, difficulty: int) -> int:
    return max(1, min(5, 6 - importance + max(0, difficulty - 3)))


def formula_for(prefix: str, index: int) -> list[str]:
    mapping = {
        "COMPLEXITY": ["T(n) 通常保留最高阶项", "O(1) < O(log n) < O(n) < O(n log n) < O(n^2)"],
        "LIST": ["顺序表插入平均移动 n/2 个元素", "单链表查找时间复杂度为 O(n)"],
        "STACK": ["栈遵循后进先出 LIFO", "循环队列长度为 (rear - front + maxsize) % maxsize"],
        "STRING": ["KMP利用 next 数组避免主串指针回退", "行优先地址按低维下标变化最快计算"],
        "TREE": ["二叉树第 i 层最多有 2^{i-1} 个结点", "任意非空二叉树满足 n0 = n2 + 1"],
        "GRAPH": ["邻接矩阵空间复杂度 O(n^2)", "Dijkstra每轮选取当前最短的未确定顶点"],
        "SEARCH": ["折半查找要求线性表有序且顺序存储", "装填因子影响哈希表查找效率"],
        "SORT": ["快速排序平均时间复杂度 O(n log n)", "稳定排序不改变相等关键字的相对次序"],
    }
    return mapping.get(prefix, [])[: 1 + index % 2]


def mistakes_for(concept_id: str) -> list[str]:
    return [
        "只记结论不理解适用条件",
        "忽略边界情况或空结构情况",
        "把相似概念的操作步骤混用",
    ]


def atomic_children(concepts: list[dict], concept_id: str) -> list[dict]:
    return [item for item in concepts if item.get("parent_id") == concept_id and item.get("granularity") == "atomic"]


def build_errors(concepts: list[dict]) -> list[dict]:
    errors = []
    atomic_by_module: dict[str, list[dict]] = {}
    for concept in concepts:
        if concept.get("granularity") == "atomic":
            atomic_by_module.setdefault(concept["module"], []).append(concept)

    for module, (prefix, quota) in ERROR_QUOTAS.items():
        atomic_items = atomic_by_module[module]
        for index in range(quota):
            concept = atomic_items[(index * len(atomic_items)) // quota]
            pattern_name, pattern_desc = ERROR_PATTERNS[index % len(ERROR_PATTERNS)]
            eid = f"ERR_{prefix}_{index + 1:03d}"
            name = f"{concept['name']}{pattern_name}"
            related = [concept["id"]]
            if index % 3 == 0 and len(atomic_items) > 1:
                related.append(atomic_items[(index + 1) % len(atomic_items)]["id"])
            errors.append(
                {
                    "error_id": eid,
                    "name": name,
                    "related_knowledge": related,
                    "error_description": f"学生在处理“{concept['name']}”时出现{pattern_name}：{pattern_desc}",
                    "typical_behavior": [
                        f"看到“{concept['name']}”相关题干时直接套模板",
                        "无法说明关键条件、步骤或中间状态为什么成立",
                        "题目变换表述后仍出现同类错误",
                    ],
                    "diagnosis_rule": f"如果错题绑定 {', '.join(related)}，且学生答案体现{pattern_name}，则触发该错因。",
                    "remediation": [
                        f"回看“{concept['name']}”的定义、适用条件和关键步骤",
                        "完成 2 道概念辨析题和 2 道过程跟踪题",
                        "复盘本错因对应的题干触发词和边界条件",
                    ],
                }
            )
    concept_by_id = {item["id"]: item for item in concepts}
    covered_ids = {kid for error in errors for kid in error["related_knowledge"]}
    for eid, name, concept_id, description in SUPPLEMENTAL_ERROR_ATOMICS:
        if concept_id in covered_ids or concept_id not in concept_by_id:
            continue
        concept = concept_by_id[concept_id]
        errors.append(
            {
                "error_id": eid,
                "name": name,
                "related_knowledge": [concept_id],
                "error_description": description,
                "typical_behavior": [
                    f"在{concept['name']}题目中把 front == rear 判断为队满",
                    "不能写出 (rear + 1) % maxsize == front 的判满条件",
                ],
                "diagnosis_rule": f"如果错题绑定 {concept_id}，且学生将队空、队满条件混用，则触发该错因。",
                "remediation": [
                    "对比循环队列判空、判满和长度计算三个公式",
                    "完成 3 道 front/rear 状态判断题并写出取模过程",
                ],
            }
        )
    return errors


def build_questions(concepts: list[dict]) -> list[dict]:
    errors = build_errors(concepts)
    error_by_concept: dict[str, str] = {}
    error_by_parent: dict[str, str] = {}
    error_by_module: dict[str, str] = {}
    concept_by_id = {item["id"]: item for item in concepts}
    for error in errors:
        for cid in error["related_knowledge"]:
            error_by_concept.setdefault(cid, error["error_id"])
            parent_id = concept_by_id[cid].get("parent_id")
            if parent_id:
                error_by_parent.setdefault(parent_id, error["error_id"])
            module = concept_by_id[cid]["module"]
            error_by_module.setdefault(module, error["error_id"])
    questions: list[dict] = []
    qtypes = ["选择题", "判断题", "填空题", "计算题", "算法执行题", "代码填空题", "综合分析题"]
    atomic_concepts = [item for item in concepts if item.get("granularity") == "atomic"]
    for idx, concept in enumerate(atomic_concepts, start=1):
        question_count = 4 if concept.get("exam_frequency", 0) >= 5 else 3
        for variant in range(question_count):
            qid = f"Q_{concept['id'].replace('DS_', 'DS_')}_{variant + 1:03d}"
            qtype = qtypes[(idx + variant) % len(qtypes)]
            if qtype == "判断题":
                stem = f"判断：复习{concept['name']}时，只记住结论即可，不必说明适用条件和边界情况。"
                answer = "错误"
                options = ["正确", "错误"]
            elif qtype == "填空题":
                stem = f"{concept['name']}属于“{concept['topic']}”主题，解题时应首先确认____。"
                answer = "适用条件"
                options = []
            elif qtype == "计算题":
                stem = f"给出一道涉及{concept['name']}的手算题，说明应如何记录关键中间状态并得到结论。"
                answer = "先列出题目条件，再按规则逐步更新中间状态，最后检查边界条件。"
                options = []
            elif qtype == "算法执行题":
                stem = f"执行与{concept['name']}相关的算法时，若当前步骤出现分支，应优先依据什么规则选择下一步？"
                answer = "依据该原子知识点的适用条件、访问顺序或更新规则选择下一步，并记录状态变化。"
                options = []
            elif qtype == "代码填空题":
                stem = f"在实现{concept['name']}时，代码空缺处通常应补入对____的判断或更新。"
                answer = "边界条件、指针位置或状态变量"
                options = []
            elif qtype == "综合分析题":
                stem = f"请结合一个期末题场景，分析{concept['name']}可能触发的错因，并给出规避方法。"
                answer = "先定位原子知识点，再说明容易混淆的条件或步骤，最后给出检查方法。"
                options = []
            else:
                stem = f"关于{concept['name']}，下列说法较合理的是哪一项？"
                answer = "需要同时掌握定义、操作过程和适用条件"
                options = [
                    "只需背诵名称即可",
                    "需要同时掌握定义、操作过程和适用条件",
                    "所有题目都可以不分析边界条件",
                    "复杂度与输入规模无关",
                ]
            error_id = error_by_concept.get(
                concept["id"],
                error_by_parent.get(concept.get("parent_id"), error_by_module[concept["module"]]),
            )
            questions.append(
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "difficulty": max(1, min(5, concept["difficulty"] + (variant % 2))),
                    "stem": stem,
                    "options": options,
                    "answer": answer,
                    "analysis": f"本题考查原子知识点“{concept['name']}”。复习时要把概念、操作步骤、适用条件和常见错因结合起来，不能只记关键词。",
                    "knowledge_points": [concept["id"]],
                    "common_errors": [error_id],
                    "exam_frequency": max(1, min(5, concept["exam_frequency"])),
                    "estimated_time": 2 if concept["difficulty"] <= 3 else 4,
                    "tags": [concept["module"], concept["topic"], concept["level"], qtype],
                }
            )
    return questions


def build_relations(concepts: list[dict]) -> list[dict]:
    relations = []
    ids = {c["id"] for c in concepts}
    concept_by_id = {c["id"]: c for c in concepts}
    for concept in concepts:
        parent = concept.get("parent_id")
        if parent in ids:
            relations.append(
                {
                    "source": parent,
                    "relation": "parent_child",
                    "target": concept["id"],
                    "description": f"{concept['id']} 是 {parent} 下的{concept.get('granularity')}粒度节点。",
                }
            )
    for concept in concepts:
        for pre in concept["prerequisites"]:
            if pre in ids:
                relations.append(
                    {
                        "source": pre,
                        "relation": "prerequisite",
                        "target": concept["id"],
                        "description": f"{pre} 是学习 {concept['id']} 前应先掌握的知识。",
                    }
                )
    explicit = [
        ("DS_LIST_001_A02", "contrast_with", "DS_LIST_002_A02", "顺序表和单链表在插入删除代价与指针维护上形成典型对比。"),
        ("DS_STACK_005_A02", "frequently_tested_with", "DS_STACK_005_A03", "循环队列判满条件常与长度计算共同考查。"),
        ("DS_STACK_005_A04", "used_in", "DS_GRAPH_003_A02", "队列入队出队规则是 BFS 队列实现的基础。"),
        ("DS_GRAPH_003_A04", "similar_to", "DS_TREE_002_A04", "BFS 与二叉树层序遍历都体现逐层访问思想。"),
        ("DS_GRAPH_002_A03", "used_in", "DS_GRAPH_001_A02", "DFS 可用于图的连通性判断。"),
        ("DS_TREE_002_A01", "frequently_tested_with", "DS_TREE_003_A01", "先序遍历规则常与先序中序还原共同考查。"),
        ("DS_TREE_005_A02", "used_in", "DS_TREE_005_A01", "哈夫曼树构造用于生成哈夫曼编码。"),
        ("DS_GRAPH_005_A02", "contrast_with", "DS_GRAPH_005_A03", "Dijkstra 松弛更新与 Floyd 中间顶点更新粒度不同。"),
        ("DS_SORT_005_A03", "frequently_tested_with", "DS_SORT_002_A02", "排序稳定性常与具体交换排序过程共同考查。"),
    ]
    for source, relation, target, description in explicit:
        if source in ids and target in ids:
            relations.append({"source": source, "relation": relation, "target": target, "description": description})
    for error in build_errors(concepts):
        for concept_id in error["related_knowledge"]:
            if concept_id in ids:
                parent_id = concept_by_id[concept_id].get("parent_id")
                if parent_id not in ids:
                    continue
                relations.append(
                    {
                        "source": concept_id,
                        "relation": "error_related_to",
                        "target": parent_id,
                        "description": f"{concept_id} 的错题可触发 {error['error_id']}：{error['name']}。",
                    }
                )
    for concept in concepts:
        if concept.get("granularity") == "concept":
            children = atomic_children(concepts, concept["id"])
            for left, right in zip(children, children[1:]):
                relations.append(
                    {
                        "source": left["id"],
                        "relation": "frequently_tested_with",
                        "target": right["id"],
                        "description": f"{left['name']} 和 {right['name']} 常在同一知识点下连续考查。",
                    }
                )
    return clean_relations(relations, ids)


def clean_relations(relations: list[dict], valid_ids: set[str]) -> list[dict]:
    high_value = {
        "parent_child",
        "prerequisite",
        "frequently_tested_with",
        "contrast_with",
        "error_related_to",
        "used_in",
        "similar_to",
    }
    cleaned = []
    seen = set()
    for relation in relations:
        source = relation.get("source")
        target = relation.get("target")
        relation_type = relation.get("relation")
        if source == target:
            continue
        if source not in valid_ids or target not in valid_ids:
            continue
        if relation_type not in high_value:
            continue
        key = (source, relation_type, target)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(relation)
    return cleaned


def build_learning_paths() -> list[dict]:
    return [
        {
            "path_id": "PATH_FOUNDATION_REPAIR_DS",
            "name": "基础补救型复习路径",
            "target_user": "基础薄弱、需要重新建立数据结构知识框架的学生",
            "sequence": ["算法与复杂度", "线性表", "栈与队列", "树与二叉树基础", "查找基础", "排序基础"],
            "strategy": "先补定义和基本操作，再用少量典型题建立信心。",
            "daily_plan": "每天 1 到 2 个基础主题，每个主题完成 5 道基础题。",
        },
        {
            "path_id": "PATH_FINAL_REVIEW_DS",
            "name": "期末冲刺型复习路径",
            "target_user": "已经学过课程，需要在短时间内系统复习的学生",
            "sequence": ["复杂度分析", "链表算法题", "栈和队列应用", "二叉树遍历与还原", "图的最小生成树和最短路径", "查找与哈希表", "排序算法综合比较"],
            "strategy": "围绕高频考点集中复习，配合错题诊断。",
            "daily_plan": "每天 2 个高频模块，每个模块 10 到 15 道题。",
        },
        {
            "path_id": "PATH_HIGH_SCORE_DS",
            "name": "高分提升型复习路径",
            "target_user": "基础较好、希望提升综合题和算法题得分的学生",
            "sequence": ["递归复杂度", "链表综合操作", "KMP", "遍历序列还原", "图算法综合", "哈希查找", "排序稳定性与复杂度比较"],
            "strategy": "聚焦难点和综合应用，要求写出完整推导或操作过程。",
            "daily_plan": "每天 1 个难点主题，完成 3 道综合题并复盘错因。",
        },
    ]


def build_student_mastery(concepts: list[dict]) -> list[dict]:
    samples = []
    scores = [0.32, 0.55, 0.76, 0.91]
    atomic_concepts = [item for item in concepts if item.get("granularity") == "atomic"]
    for i, concept in enumerate(atomic_concepts[:48]):
        score = scores[i % len(scores)]
        status = "not_mastered" if score < 0.4 else "partially_mastered" if score < 0.7 else "basically_mastered" if score < 0.9 else "mastered"
        samples.append(
            {
                "student_id": "S001",
                "knowledge_id": concept["id"],
                "mastery_score": score,
                "attempt_count": 8 + i,
                "correct_count": int((8 + i) * score),
                "recent_error_count": max(0, 4 - i % 5),
                "last_review_time": "2026-05-14",
                "status": status,
            }
        )
    return samples


def main() -> None:
    concepts = build_concepts()
    dump("concepts.json", concepts)
    dump("errors.json", build_errors(concepts))
    dump("questions.json", build_questions(concepts))
    dump("relations.json", build_relations(concepts))
    dump("learning_paths.json", build_learning_paths())
    dump("student_mastery_sample.json", build_student_mastery(concepts))


if __name__ == "__main__":
    main()
