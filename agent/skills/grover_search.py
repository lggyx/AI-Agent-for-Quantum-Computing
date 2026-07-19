"""
Skill: grover_search — Grover搜索算法
"""

from pathlib import Path

from unitarylab_algorithms import GroverAlgorithm


def run(args: dict) -> dict:
    n = args.get("n", 3)
    target = args.get("target", "101")
    device = args.get("device", "gpu")

    try:
        algo = GroverAlgorithm(text_mode="legacy")
        result = algo.run(n=n, target=target, device=device)
    except Exception as e:
        # fallback to cpu
        algo = GroverAlgorithm(text_mode="legacy")
        result = algo.run(n=n, target=target, device="cpu")

    status = result.get("status", "unknown")
    ok = status in ("ok", "success", "partial_success")
    prob = result.get("Amplified target-state probability", result.get("summary", "N/A"))

    # 解析摘要
    summary = result.get("summary", "")
    if isinstance(summary, str) and summary:
        lines = summary.split("\n")
        short_summary = "\n".join(f"  {l.strip()}" for l in lines if l.strip())
    else:
        short_summary = f"Grover搜索目标 |{target}⟩ 完成"

    # 安全过滤不可序列化的字段
    raw = {}
    for k, v in result.items():
        try:
            import json
            json.dumps(v)
            raw[k] = v
        except (TypeError, ValueError):
            raw[k] = str(v)

    return {
        "status": "ok" if ok else "error",
        "summary": (
            f"Grover搜索算法\n"
            f"  搜索空间: {n} 量子比特 ({2**n} 个态)\n"
            f"  目标态: |{target}⟩\n"
            f"  结果: {'✅ 搜索成功' if ok else '❌ 搜索失败'}\n"
            f"{short_summary}"
        ),
        "results": {
            "n": n,
            "target": target,
            "status": status,
            "raw": raw,
            "circuit_path": result.get("circuit_path"),
        },
        "visualization": result.get("circuit_path"),
    }