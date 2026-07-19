"""
Skill: visualize — 结果可视化

从已有的运行结果文件生成图表。
"""

import json
from pathlib import Path

import numpy as np


def run(args: dict) -> dict:
    data = args.get("data", args.get("text", ""))
    result_type = args.get("type", "auto")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return {
            "status": "error",
            "summary": "Matplotlib 未安装，无法生成可视化",
            "results": {},
        }

    out_dir = Path("quantum/results/plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 尝试加载结果文件
    if data and Path(data).exists():
        try:
            result = json.loads(Path(data).read_text())
        except Exception:
            result = {"_raw": data}
    else:
        # 查找最新结果文件
        result_files = sorted(Path("quantum/results").rglob("*.json"))
        if result_files:
            result = json.loads(result_files[-1].read_text())
        else:
            return {
                "status": "error",
                "summary": "未找到结果数据",
                "results": {},
            }

    # 智能判断数据类型并绘图
    fig = None
    path = None

    if "cpu_probs" in result or "probabilities" in result:
        probs = result.get("cpu_probs") or result.get("probabilities", [])
        fig, ax = plt.subplots(figsize=(6, 4))
        n = len(probs)
        n_bits = max(1, (n.bit_length() - 1))
        labels = [f"|{i:0{n_bits}b}⟩" for i in range(n)]
        colors = ["#4CAF50" if p > 0.01 else "#BDBDBD" for p in probs]
        ax.bar(labels, probs, color=colors, edgecolor="gray")
        ax.set_ylim(0, max(probs) * 1.2)
        ax.set_ylabel("Probability")
        ax.set_title("Quantum State Probability Distribution")
        for i, p in enumerate(probs):
            ax.text(i, p + 0.01, f"{p:.3f}", ha="center", fontsize=8)
        path = str(out_dir / "visualize_probs.png")

    elif "final_loss" in result or "final_accuracy" in result:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        loss = result.get("final_loss", 0)
        acc = result.get("final_accuracy", 0)
        ax1.bar(["Final Loss"], [loss], color="#F44336")
        ax1.set_ylabel("Loss")
        ax1.set_title("VQC Training Loss")
        ax2.bar(["Final Accuracy"], [acc * 100 if acc <= 1 else acc], color="#4CAF50")
        ax2.set_ylabel("Accuracy (%)")
        ax2.set_title("VQC Classification Accuracy")
        path = str(out_dir / "visualize_vqc.png")

    elif "max_abs_diff" in result:
        fig, ax = plt.subplots(figsize=(6, 4))
        diff = result.get("max_abs_diff", 0)
        ax.bar(["Max Abs Diff"], [diff], color="#FF9800")
        ax.set_ylabel("Error")
        ax.set_title("Backend Comparison Error")
        ax.text(0, diff + 1e-6, f"{diff:.2e}", ha="center")
        path = str(out_dir / "visualize_compare.png")

    else:
        # 通用文本摘要
        return {
            "status": "ok",
            "summary": f"结果数据摘要:\n" + json.dumps(result, indent=2, ensure_ascii=False)[:500],
            "results": {"data_preview": result},
        }

    if fig:
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return {
            "status": "ok",
            "summary": f"可视化已保存: {path}",
            "results": {"path": path},
            "visualization": path,
        }

    return {
        "status": "ok",
        "summary": "无合适的数据格式用于可视化",
        "results": {},
    }