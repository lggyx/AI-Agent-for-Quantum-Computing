import json
from pathlib import Path

import numpy as np
import torch
from unitarylab import Circuit


def build_bell_circuit():
    circuit = Circuit(2, name="bell_state")
    circuit.h(0)
    circuit.cx(0, 1)
    return circuit


def run(device: str):
    circuit = build_bell_circuit()
    state = circuit.execute(device=device).state
    probs = np.abs(state) ** 2
    return probs


def main():
    cpu_probs = run("cpu")
    gpu_probs = run("gpu")

    result = {
        "task": "bell_state_demo",
        "torch": torch.__version__,
        "cpu_probs": cpu_probs.tolist(),
        "gpu_probs": gpu_probs.tolist(),
        "max_abs_diff": float(np.max(np.abs(cpu_probs - gpu_probs))),
        "ok": bool(np.allclose(cpu_probs, gpu_probs, atol=1e-5)),
    }

    Path("results").mkdir(exist_ok=True)
    Path("results/bell_state_result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    assert result["ok"]


if __name__ == "__main__":
    main()
