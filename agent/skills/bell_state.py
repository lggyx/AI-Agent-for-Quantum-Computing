"""
Skill: bell_state — Bell态制备与测量
"""

from pathlib import Path

import numpy as np
from unitarylab import Circuit


def run(args: dict) -> dict:
    device = args.get("device", None)  # None = both cpu & gpu for comparison

    cpu_probs = _run_on("cpu")
    vis_paths = []

    if device == "cpu":
        gpu_probs = None
        probs = cpu_probs
        max_diff = 0.0
        ok = True
    else:
        gpu_probs = _run_on("gpu")
        probs = gpu_probs
        max_diff = float(np.max(np.abs(cpu_probs - gpu_probs)))
        ok = bool(np.allclose(cpu_probs, gpu_probs, atol=1e-5))

    # 生成可视化：概率分布图 + 线路图
    probs_vis = _plot_probs(probs, cpu_probs, gpu_probs, max_diff)
    if probs_vis:
        vis_paths.append(probs_vis)
    circuit_vis = _plot_circuit()
    if circuit_vis:
        vis_paths.append(circuit_vis)

    summary_parts = [
        f"Bell态制备完成\n"
        f"  线路: H(0), CNOT(0,1)\n"
        f"  测量结果:",
    ]
    state_names = [f"|{i:02b}⟩" for i in range(4)]
    for i, p in enumerate(probs):
        if p > 0.01:
            summary_parts.append(f"    {state_names[i]}: {p*100:.2f}%")
    if gpu_probs is not None:
        summary_parts.append(f"  CPU vs GPU 最大误差: {max_diff:.2e}")
        summary_parts.append(f"  {'✅ CPU与GPU结果一致' if ok else '❌ 结果不一致'}")

    return {
        "status": "ok" if ok else "error",
        "summary": "\n".join(summary_parts),
        "results": {
            "cpu_probs": cpu_probs.tolist(),
            "gpu_probs": gpu_probs.tolist() if gpu_probs is not None else None,
            "max_abs_diff": max_diff,
            "consistent": ok,
            "probs_vis": probs_vis,
            "circuit_vis": circuit_vis,
        },
        "visualization": probs_vis,
    }


def _run_on(device: str) -> np.ndarray:
    circuit = Circuit(2, name="bell_state")
    circuit.h(0)
    circuit.cx(0, 1)
    state = circuit.execute(device=device).state
    return np.abs(state) ** 2


def _plot_probs(probs: np.ndarray, cpu_probs: np.ndarray, gpu_probs: np.ndarray | None, max_diff: float) -> str | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        states = [f"|{i:02b}⟩" for i in range(4)]
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["#4CAF50" if p > 0.01 else "#BDBDBD" for p in probs]
        bars = ax.bar(states, probs, color=colors, edgecolor="gray", linewidth=1.5)
        ax.set_ylim(0, 1.15)
        ax.set_ylabel("Probability", fontsize=12)
        ax.set_xlabel("Basis State", fontsize=12)

        # 标题：显示对比信息
        title = "Bell State |Φ⁺⟩ = (|00⟩ + |11⟩)/√2"
        if gpu_probs is not None:
            title += f"\nCPU vs GPU max error: {max_diff:.2e}"
            if max_diff < 1e-5:
                title += "  ✅ Consistent"
            else:
                title += "  ❌ Mismatch"
        ax.set_title(title, fontsize=13, fontweight="bold")

        # 柱顶标注
        for bar, p in zip(bars, probs):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{p*100:.1f}%", ha="center", fontsize=11, fontweight="bold")

        # 理论值虚线
        ax.axhline(y=0.5, color="red", linestyle="--", alpha=0.5, label="Theoretical (50%)")
        ax.legend(fontsize=10)

        out_dir = Path("quantum/results/plots")
        out_dir.mkdir(parents=True, exist_ok=True)
        path = str(out_dir / "bell_state_probs.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path
    except ImportError:
        return None
    except Exception:
        return None


def _plot_circuit() -> str | None:
    """生成 Bell 态 ASCII 线路图"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.set_xlim(-0.5, 7)
        ax.set_ylim(-1.5, 1.5)
        ax.axis("off")
        ax.set_title("Bell State Circuit: H(0) + CNOT(0,1)", fontsize=13, fontweight="bold", pad=15)

        # 量子比特线
        for i, (name, y) in enumerate([("|q₀⟩", 0.8), ("|q₁⟩", -0.8)]):
            ax.annotate(name, xy=(-0.3, y), fontsize=12, ha="right", va="center")
            ax.plot([0, 6.5], [y, y], color="#555", linewidth=1.5)

        # H 门
        h_rect = patches.FancyBboxPatch((0.8, 0.35), 0.8, 0.9, boxstyle="round,pad=0.1",
                                         facecolor="#6C8CFF", edgecolor="#4a6adf", linewidth=2)
        ax.add_patch(h_rect)
        ax.text(1.2, 0.8, "H", ha="center", va="center", fontsize=14, fontweight="bold", color="white")

        # CNOT 控制点
        ax.plot(3, 0.8, "o", color="#E74C3C", markersize=14, zorder=5)
        # CNOT 连线
        ax.plot([3, 3], [-0.8, 0.8], color="#E74C3C", linewidth=2)
        # CNOT 目标点
        circle = plt.Circle((3, -0.8), 0.3, fill=False, edgecolor="#E74C3C", linewidth=2.5)
        ax.add_patch(circle)
        ax.plot(3, -0.8, "x", color="#E74C3C", markersize=10)

        # 测量符号
        for y in [0.8, -0.8]:
            meter = patches.FancyBboxPatch((5.2, y - 0.35), 0.8, 0.7, boxstyle="round,pad=0.1",
                                           facecolor="#2C3E50", edgecolor="#888", linewidth=1.5)
            ax.add_patch(meter)
            ax.text(5.6, y, "M", ha="center", va="center", fontsize=12, fontweight="bold", color="#ddd")

        # 时间箭头
        ax.annotate("", xy=(6.8, 0), xytext=(-0.2, 0),
                    arrowprops=dict(arrowstyle="->", color="#888", lw=1), alpha=0.5)
        ax.text(6.9, 0, "t", fontsize=10, color="#888", va="center")

        out_dir = Path("quantum/results/plots")
        out_dir.mkdir(parents=True, exist_ok=True)
        path = str(out_dir / "bell_state_circuit.svg")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path
    except ImportError:
        return None
    except Exception:
        return None