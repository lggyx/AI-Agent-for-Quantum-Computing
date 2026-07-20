"""
Skill: vqc_classify — VQC变分量子分类
"""

from unitarylab_algorithms import VQCAlgorithm


def run(args: dict) -> dict:
    layers = args.get("layers", 2)       # 默认 2 层（原 1 层），提高表达能力
    epochs = args.get("epochs", 10)      # 默认 10 epoch（原 3），充分训练
    lr = args.get("lr", 0.05)
    batch_size = args.get("batch_size", 4)
    device = args.get("device", "gpu")

    algo = VQCAlgorithm(text_mode="legacy")
    result = algo.run(
        layers=layers,
        epochs=epochs,
        lr=lr,
        batch_size=batch_size,
        device=device,
    )

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