"""
Skill: vqc_classify — VQC变分量子分类

注意：壁仞 GPU (torch_br) 存在显存泄漏问题，连续调用 GPU 训练会崩溃。
解决方案：通过子进程隔离每次 GPU 训练，进程退出后显存自动回收。
"""

import subprocess
import sys
import json
from pathlib import Path


def run(args: dict) -> dict:
    layers = args.get("layers", 2)       # 默认 2 层，提高表达能力
    epochs = args.get("epochs", 10)      # 默认 10 epoch，充分训练
    lr = args.get("lr", 0.01)            # 默认学习率 0.01（原 0.05）更稳定
    batch_size = args.get("batch_size", 4)
    device = args.get("device", "gpu")

    # 如果是 CPU 设备，直接本地运行（无泄漏问题）
    if device == "cpu":
        return _run_local(layers, epochs, lr, batch_size)

    # GPU 设备：通过子进程隔离，避免 torch_br 显存泄漏
    return _run_subprocess(layers, epochs, lr, batch_size, device)


def _run_local(layers: int, epochs: int, lr: float, batch_size: int) -> dict:
    """本地进程运行 VQC（适用于 CPU）"""
    from unitarylab_algorithms import VQCAlgorithm

    algo = VQCAlgorithm(text_mode="legacy")
    result = algo.run(
        layers=layers,
        epochs=epochs,
        lr=lr,
        batch_size=batch_size,
        device="cpu",
    )

    return _format_result(result, layers, epochs, lr, batch_size)


def _run_subprocess(layers: int, epochs: int, lr: float, batch_size: int, device: str) -> dict:
    """子进程隔离运行 VQC（适用于 GPU，规避显存泄漏）"""
    code = f"""
import sys, json
sys.path.insert(0, {repr(str(Path(__file__).resolve().parent.parent.parent))})
from unitarylab_algorithms import VQCAlgorithm
algo = VQCAlgorithm(text_mode='legacy')
result = algo.run(
    layers={layers}, epochs={epochs}, lr={lr},
    batch_size={batch_size}, device={repr(device)},
)
# 只输出可序列化的结果
output = {{
    k: v for k, v in result.items()
    if k in ('status', 'Final Loss', 'Final Accuracy', 'Quantal Computation Time (s)',
             'circuit_path', 'file_path')
}}
print('__VQC_RESULT__' + json.dumps(output))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=360,
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "summary": f"VQC训练超时 (layers={layers}, epochs={epochs}, device={device})",
            "results": {"error": "timeout"},
        }

    # 解析子进程输出
    stdout = proc.stdout
    stderr = proc.stderr

    for line in stdout.split("\n"):
        if line.startswith("__VQC_RESULT__"):
            try:
                result = json.loads(line[len("__VQC_RESULT__"):])
                return _format_result(result, layers, epochs, lr, batch_size)
            except json.JSONDecodeError:
                pass

    # 子进程失败
    error_msg = stderr.split("\n")[-3:] if stderr else ["unknown error"]
    return {
        "status": "error",
        "summary": f"VQC训练执行失败 (子进程)\n  {error_msg}",
        "results": {"error": "subprocess_failed", "stderr": stderr[:500]},
    }


def _format_result(result: dict, layers: int, epochs: int, lr: float, batch_size: int) -> dict:
    """统一格式化 VQC 结果"""
    status = result.get("status", "unknown")
    ok = status in ("ok", "success", "partial_success")
    final_loss = result.get("Final Loss", "N/A")
    final_acc = result.get("Final Accuracy", "N/A")
    quantum_time = result.get("Quantal Computation Time (s)", "N/A")

    if isinstance(final_loss, float):
        loss_str = f"{final_loss:.4f}"
    else:
        loss_str = str(final_loss)

    if isinstance(final_acc, float):
        acc_str = f"{final_acc*100:.1f}%" if final_acc <= 1 else f"{final_acc:.1f}%"
    else:
        acc_str = str(final_acc)

    return {
        "status": "ok" if ok else "error",
        "summary": (
            f"VQC变分量子分类器训练\n"
            f"  训练配置: layers={layers}, epochs={epochs}, lr={lr}, batch={batch_size}\n"
            f"  最终损失: {loss_str}\n"
            f"  最终准确率: {acc_str}\n"
            f"  量子计算时间: {quantum_time}s\n"
            f"  {'✅ 训练完成' if ok else '❌ 训练异常'}"
        ),
        "results": {
            "layers": layers,
            "epochs": epochs,
            "lr": lr,
            "status": status,
            "final_loss": final_loss,
            "final_accuracy": final_acc,
            "quantum_time_s": quantum_time,
        },
    }