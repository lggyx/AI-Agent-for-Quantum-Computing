"""
Skill: circuit_builder — 自定义量子线路

从自然语言描述构建任意量子线路并执行。
支持的门: H, X, Y, Z, CX/CNOT, RX, RY, RZ, Measure
"""

import re

import numpy as np
from unitarylab import Circuit


def run(args: dict) -> dict:
    text = args.get("text", args.get("gates", ""))
    device = args.get("device", "gpu")
    qubits = args.get("qubits", None)

    # 从自然语言中提取门序列
    gates = _parse_gates(text)
    if not gates:
        return {
            "status": "error",
            "summary": "无法解析线路描述。示例: 'h(0), cx(0,1), measure all'",
            "results": {},
        }

    if qubits is None:
        # 自动推断 qubit 数
        max_q = 0
        for g in gates:
            for q in g["targets"]:
                max_q = max(max_q, q + 1)
        qubits = max(2, max_q)

    # 构建线路
    circuit = Circuit(qubits, name="custom_circuit")
    for g in gates:
        gate = g["gate"].lower()
        targets = g["targets"]
        params = g.get("params", [])

        if gate in ("h", "hadamard"):
            circuit.h(targets[0])
        elif gate in ("x", "not", "pauli-x"):
            circuit.x(targets[0])
        elif gate in ("y", "pauli-y"):
            circuit.y(targets[0])
        elif gate in ("z", "pauli-z"):
            circuit.z(targets[0])
        elif gate in ("cx", "cnot") and len(targets) >= 2:
            circuit.cx(targets[0], targets[1])
        elif gate == "cz" and len(targets) >= 2:
            circuit.cz(targets[0], targets[1])
        elif gate in ("rx",) and len(params) >= 1:
            circuit.rx(targets[0], params[0])
        elif gate in ("ry",) and len(params) >= 1:
            circuit.ry(targets[0], params[0])
        elif gate in ("rz",) and len(params) >= 1:
            circuit.rz(targets[0], params[0])
        elif gate in ("measure", "m"):
            pass  # simulate automatically measures at end
        else:
            raise ValueError(f"不支持的门: {gate}")

    # 执行
    try:
        state = circuit.execute(device=device).state
    except Exception:
        state = circuit.execute(device="cpu").state

    probs = np.abs(state) ** 2

    # 格式化结果
    n = qubits
    top_n = min(8, 2**n)
    probs_list = probs.tolist()
    top_indices = np.argsort(probs)[-top_n:][::-1]
    prob_lines = []
    for idx in top_indices:
        if probs[idx] > 1e-4:
            prob_lines.append(f"    |{idx:0{n}b}⟩: {probs[idx]*100:.2f}%")

    return {
        "status": "ok",
        "summary": (
            f"自定义量子线路\n"
            f"  量子比特数: {qubits}\n"
            f"  门序列: {', '.join(g['gate'] for g in gates)}\n"
            f"  设备: {device}\n"
            f"  线路结果 (Top {top_n}):\n"
            + "\n".join(prob_lines)
        ),
        "results": {
            "qubits": qubits,
            "gates": [{"gate": g["gate"], "targets": g["targets"], "params": g.get("params", [])} for g in gates],
            "state_vector": (state[:16].tolist() if len(state) > 16 else state.tolist()),
            "probabilities": probs_list[:16] if len(probs_list) > 16 else probs_list,
            "truncated": len(state) > 16,
        },
    }


def _parse_gates(text: str) -> list[dict]:
    """解析自然语言描述中的门序列"""
    gates = []

    # 移除常见前缀/后缀
    text = re.sub(r'(?:构建|创建|create|build|线路|circuit)[：:\s]*', '', text, flags=re.IGNORECASE)

    # 按逗号/分号/空格切分门序列
    parts = re.split(r'[;,，；]\s*', text)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 匹配: gate(q) 或 gate q 或 gate(q, params...)
        m = re.match(r'(\w+)\s*\(([^)]*)\)', part)
        if m:
            gate_name = m.group(1)
            args_str = m.group(2)
            args_list = [a.strip() for a in args_str.split(",") if a.strip()]

            targets = []
            params = []
            for a in args_list:
                try:
                    params.append(float(a))
                except ValueError:
                    targets.append(int(a))

            if not targets:
                targets = [0]

            gates.append({"gate": gate_name, "targets": targets, "params": params})
        else:
            # 格式: H 0, CX 0 1, measure all
            words = part.split()
            if len(words) >= 2:
                gate_name = words[0]
                rest = words[1:]
                if "all" in rest or "all" in gate_name.lower():
                    continue  # measure all — skip, auto-measured
                targets = []
                params = []
                for w in rest:
                    try:
                        params.append(float(w))
                    except ValueError:
                        targets.append(int(w))
                if not targets:
                    targets = [0]
                gates.append({"gate": gate_name, "targets": targets, "params": params})

    return gates