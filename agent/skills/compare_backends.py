"""
Skill: compare_backends — SUPA vs UnitaryLab 对比验证

注意：SUPA 依赖壁仞 BIRENSUPA SDK，无 SDK 时仅报告环境不可用。
"""

from pathlib import Path

import numpy as np
from unitarylab import Circuit
from unitarylab_algorithms import GroverAlgorithm


def run(args: dict) -> dict:
    # 仅运行 UnitaryLab 部分
    bell_ref = _unitarylab_bell_probs()
    grover_ref = _unitarylab_grover()

    # 检查是否有 SUPA 编译产物
    supa_bin = Path("quantum/examples/supa/quantum_reference.out")
    supa_available = supa_bin.exists()

    if supa_available:
        import subprocess
        import json
        try:
            out = subprocess.check_output([str(supa_bin)], text=True)
            supa = json.loads(out)
            bell_supa = np.array(supa["bell_probs"], dtype=np.float32)
            grover_supa = float(supa["grover_target_probability"])

            bell_diff = float(np.max(np.abs(bell_ref - bell_supa)))
            grover_diff = abs(float(grover_ref["Amplified target-state probability"]) - grover_supa)

            ok = bell_diff <= 1e-5 and grover_diff <= 1e-5

            return {
                "status": "ok" if ok else "error",
                "summary": (
                    f"SUPA vs UnitaryLab 交叉验证\n"
                    f"  Bell态最大误差: {bell_diff:.2e} {'✅' if bell_diff <= 1e-5 else '❌'}\n"
                    f"  Grover最大误差: {grover_diff:.2e} {'✅' if grover_diff <= 1e-5 else '❌'}\n"
                    f"  {'✅ 后端结果一致' if ok else '❌ 存在差异'}"
                ),
                "results": {
                    "supa_available": True,
                    "bell_max_abs_diff": bell_diff,
                    "grover_abs_diff": grover_diff,
                    "consistent": ok,
                },
            }
        except Exception as e:
            return {
                "status": "error",
                "summary": f"SUPA 运行失败: {e}",
                "results": {"supa_available": True, "error": str(e)},
            }
    else:
        # 仅输出 UnitaryLab 基线
        return {
            "status": "env_unavailable",
            "summary": (
                "SUPA 壁仞GPU后端不可用（未检测到编译产物）\n"
                f"UnitaryLab 参考结果: Bell态 {bell_ref.tolist()}, "
                f"Grover目标概率 {grover_ref.get('Amplified target-state probability', 'N/A')}\n"
                "提示: 在壁仞SDK环境下编译 quantum/examples/supa/quantum_reference.su 后重试"
            ),
            "results": {
                "supa_available": False,
                "unitarylab_bell_probs": bell_ref.tolist(),
                "unitarylab_grover_summary": grover_ref.get("summary", ""),
            },
        }


def _unitarylab_bell_probs() -> np.ndarray:
    circuit = Circuit(2, name="bell_state")
    circuit.h(0)
    circuit.cx(0, 1)
    state = circuit.execute(device="cpu").state
    return np.abs(state) ** 2


def _unitarylab_grover() -> dict:
    algo = GroverAlgorithm(text_mode="legacy")
    return algo.run(n=3, target="101", device="cpu")