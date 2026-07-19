import json
import subprocess
from pathlib import Path

import numpy as np
from unitarylab import Circuit
from unitarylab_algorithms import GroverAlgorithm


def run_supa():
    out = subprocess.check_output(["./examples/supa/quantum_reference.out"], text=True)
    return json.loads(out)


def unitarylab_bell_probs():
    circuit = Circuit(2, name="bell_state")
    circuit.h(0)
    circuit.cx(0, 1)
    state = circuit.execute(device="cpu").state
    return np.abs(state) ** 2


def unitarylab_grover():
    algo = GroverAlgorithm(text_mode="legacy")
    return algo.run(n=3, target="101", device="cpu")


def main():
    supa = run_supa()
    bell_ref = unitarylab_bell_probs()
    grover_ref = unitarylab_grover()

    bell_supa = np.array(supa["bell_probs"], dtype=np.float32)
    grover_supa = float(supa["grover_target_probability"])
    grover_ref_prob = float(grover_ref["Amplified target-state probability"])

    report = {
        "bell_max_abs_diff": float(np.max(np.abs(bell_ref - bell_supa))),
        "grover_abs_diff": abs(grover_ref_prob - grover_supa),
        "grover_unitarylab_result": grover_ref["Result"],
        "grover_supa_result_index": supa["grover_result_index"],
    }
    report["ok"] = (
        report["bell_max_abs_diff"] <= 1e-5
        and report["grover_abs_diff"] <= 1e-5
        and report["grover_unitarylab_result"] == "101"
        and report["grover_supa_result_index"] == 5
    )

    Path("results").mkdir(exist_ok=True)
    Path("results/supa_unitarylab_compare.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    assert report["ok"]


if __name__ == "__main__":
    main()
