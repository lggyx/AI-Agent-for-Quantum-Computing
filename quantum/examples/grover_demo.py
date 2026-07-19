import json
from pathlib import Path

from unitarylab_algorithms import GroverAlgorithm


def run_grover(device: str, n: int = 3, target: str = "101"):
    algo = GroverAlgorithm(text_mode="legacy")
    return algo.run(n=n, target=target, device=device)


def pick_result(result):
    return {
        "status": result.get("status"),
        "summary": result.get("summary"),
        "circuit_path": result.get("circuit_path"),
        "raw_keys": sorted(result.keys()),
    }


def main():
    cpu = run_grover("cpu")
    gpu = run_grover("gpu")

    report = {
        "task": "grover_search_demo",
        "target": "101",
        "cpu": pick_result(cpu),
        "gpu": pick_result(gpu),
        "ok": gpu.get("status") in ("ok", "success", "partial_success"),
    }

    Path("results").mkdir(exist_ok=True)
    Path("results/grover_result.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    assert report["ok"]


if __name__ == "__main__":
    main()
