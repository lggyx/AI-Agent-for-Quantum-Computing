"""
Skill: help — 帮助信息

列出所有可用技能及其描述。
"""

from agent.skills import get_engine


def run(args: dict) -> dict:
    engine = get_engine()
    skills = engine.list_skills()

    lines = [
        "🎯 量子计算 Agent — 可用技能列表",
        "═══════════════════════════════════════════",
    ]
    for s in skills:
        if s["id"] in ("help", "list_skills"):
            continue
        lines.append(f"  {s['id']:20s}  {s['name']}")
        lines.append(f"  {'':20s}  {s['description']}")

    lines += [
        "",
        "📝 使用示例:",
        "  > Bell态演示",
        "  > Grover搜索，目标态 101",
        "  > 训练VQC，2层，5个epoch",
        "  > h(0), cx(0,1)  — 自定义线路",
        "  > 可视化 — 查看结果图表",
    ]

    return {
        "status": "ok",
        "summary": "\n".join(lines),
        "results": {"skills": skills},
    }