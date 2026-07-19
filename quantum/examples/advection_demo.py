import json
from pathlib import Path

from unitarylab_algorithms import AdvectionEquationAlgorithm


def run():
    algo = AdvectionEquationAlgorithm()
    return algo.run()


def simplify(result):
    return {
        "status": result.get("status"),
        "summary": result.get("summary"),
        "circuit_path": result.get("circuit_path"),
        "raw_keys": sorted(result.keys()),
    }


def main():
    result = run()

    report = {
        "task": "advection_equation_demo",
        "result": simplify(result),
        "ok": result.get("status") in ("ok", "success", "partial_success"),
    }

    Path("results").mkdir(exist_ok=True)
    Path("results/advection_result.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    assert report["ok"]


if __name__ == "__main__":
    main()
