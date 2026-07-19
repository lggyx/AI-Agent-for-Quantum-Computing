import json
from pathlib import Path

from unitarylab_algorithms import VQCAlgorithm


def main():
    algo = VQCAlgorithm(text_mode="legacy")
    result = algo.run(
        layers=1,
        epochs=2,
        lr=0.05,
        batch_size=4,
        device="gpu",
    )

    report = {
        "task": "vqc_classification_demo",
        "status": result.get("status"),
        "final_loss": result.get("Final Loss"),
        "final_accuracy": result.get("Final Accuracy"),
        "quantum_time_s": result.get("Quantal Computation Time (s)"),
        "raw_keys": sorted(result.keys()),
        "ok": result.get("status") in ("ok", "success", "partial_success"),
    }

    Path("results").mkdir(exist_ok=True)
    Path("results/vqc_result.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    assert report["ok"]


if __name__ == "__main__":
    main()
