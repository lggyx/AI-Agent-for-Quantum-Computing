"""
Skill: advection_sim — 平流方程量子模拟（薛定谔化方法）
"""

from unitarylab_algorithms import AdvectionEquationAlgorithm


def run(args: dict) -> dict:
    nx = args.get("nx", 4)
    na = args.get("na", 8)
    T = args.get("T", 1.0)

    algo = AdvectionEquationAlgorithm()
    result = algo.run()

    status = result.get("status", "unknown")
    ok = status in ("ok", "success", "partial_success")
    summary = result.get("summary", "")

    if isinstance(summary, str) and summary:
        lines = summary.split("\n")
        short_summary = "\n".join(f"  {l.strip()}" for l in lines if l.strip())
    else:
        short_summary = "平流方程模拟完成"

    return {
        "status": "ok" if ok else "error",
        "summary": (
            f"平流方程量子模拟（薛定谔化方法）\n"
            f"  网格: nx={nx}, na={na}, T={T}\n"
            f"  {'✅ 模拟成功' if ok else '❌ 模拟异常'}\n"
            f"{short_summary}"
        ),
        "results": {
            "nx": nx,
            "na": na,
            "T": T,
            "status": status,
            "raw_keys": sorted(result.keys()),
            "summary": summary,
            "circuit_path": result.get("circuit_path"),
        },
    }