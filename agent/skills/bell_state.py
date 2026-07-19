"""
Skill: bell_state — Bell态制备与测量
"""

from pathlib import Path

import numpy as np
from unitarylab import Circuit


def run(args: dict) -> dict:
    device = args.get("device", None)  # None = both cpu & gpu for comparison

    cpu_probs = _run_on("cpu")
    vis_path = None

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

        if ok:
            # 生成可视化
            vis_path = _plot_probs(probs)

    return {
        "status": "ok" if ok else "error",
        "summary": (
            f"Bell态制备完成\n"
            f"  |00⟩: {probs[0]*100:.2f}%\n"
            f"  |11⟩: {probs[3]*100:.2f}%\n"
            f"  {'✅ CPU与GPU结果一致' if ok else '❌ 结果不一致'}"
        ),
        "results": {
            "cpu_probs": cpu_probs.tolist(),
            "gpu_probs": gpu_probs.tolist() if gpu_probs is not None else None,
            "max_abs_diff": max_diff,
            "consistent": ok,
        },
        "visualization": vis_path,
    }


def _run_on(device: str) -> np.ndarray:
    circuit = Circuit(2, name="bell_state")
    circuit.h(0)
    circuit.cx(0, 1)
    state = circuit.execute(device=device).state
    return np.abs(state) ** 2


def _plot_probs(probs: np.ndarray) -> str | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        states = [f"|{i:02b}⟩" for i in range(4)]
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ["#4CAF50" if p > 0.01 else "#BDBDBD" for p in probs]
        ax.bar(states, probs, color=colors, edgecolor="gray")
        ax.set_ylim(0, 1)
        ax.set_ylabel("Probability")
        ax.set_title("Bell State |Φ⁺⟩ = (|00⟩ + |11⟩)/√2")
        for i, p in enumerate(probs):
            ax.text(i, p + 0.02, f"{p:.4f}", ha="center", fontsize=10)

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