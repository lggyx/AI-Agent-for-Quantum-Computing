"""
Quantum Agent CLI — 自然语言交互的统一演示平台

支持通过自然语言与 Agent 交互，完成量子线路构建、模拟执行、
结果分析与可视化展示等全流程任务。
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

from agent.skills import get_engine, SkillEngine, SkillResult


# ── ANSI 颜色 ──────────────────────────────────────────────────────

class Colors:
    HEADER = "\033[1;34m"   # 蓝色粗体
    GREEN = "\033[1;32m"    # 绿色
    YELLOW = "\033[1;33m"   # 黄色
    RED = "\033[1;31m"      # 红色
    CYAN = "\033[1;36m"     # 青色
    MAGENTA = "\033[1;35m"  # 紫色
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


def c(color: str, text: str) -> str:
    """Wrap text in ANSI color, auto-reset."""
    return f"{color}{text}{Colors.RESET}"


# ── Banner ──────────────────────────────────────────────────────────

BANNER = r"""
  ___                  _   _                _   _             _
 / _ \ _   _  __ _ ___| |_(_) ___ ___    __| | | |_ ___  __ _| | ___  ___
| | | | | | |/ _` / __| __| |/ __/ __|  / _` | | __/ _ \/ _` | |/ _ \/ __|
| |_| | |_| | (_| \__ \ |_| | (__\__ \ | (_| | | ||  __/ (_| | |  __/\__ \
 \__\_\\__,_|\__,_|___/\__|_|\___|___/  \__,_|  \__\___|\__,_|_|\___||___/
                       Quantum Computing Agent Platform
                       量子计算模拟与算法演示平台
"""


# ── 渲染 ────────────────────────────────────────────────────────────


def render_result(result: SkillResult) -> str:
    """将 SkillResult 渲染为终端友好文本"""
    status_icon = {
        "ok": c(Colors.GREEN, "✅"),
        "error": c(Colors.RED, "❌"),
        "env_unavailable": c(Colors.YELLOW, "⚠️"),
    }.get(result.status, c(Colors.YELLOW, "❓"))

    lines = [
        "",
        f"  {c(Colors.HEADER, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}",
        f"  {status_icon} {c(Colors.BOLD, result.results.get('skill', result.skill) or result.skill)}",
        f"  {c(Colors.HEADER, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}",
        f"  {c(Colors.CYAN, '状态:')}  {result.status}",
    ]

    if result.summary:
        summary_lines = result.summary.strip().split("\n")
        for line in summary_lines:
            lines.append(f"  {line}")

    if result.visualization:
        lines.append(f"  {c(Colors.MAGENTA, '📊 可视化:')} {result.visualization}")

    lines.append(f"  {c(Colors.DIM, f'⏱ 耗时: {result.duration_s:.3f}s')}")
    lines.append(f"  {c(Colors.HEADER, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}")
    lines.append("")

    return "\n".join(lines)


# ── 日志回放 ────────────────────────────────────────────────────────


def display_logs(engine: SkillEngine) -> None:
    """显示当前会话的交互日志"""
    logs = engine.get_logs()
    if not logs:
        print(f"  {c(Colors.YELLOW, '暂无交互记录')}")
        return

    print(f"\n  {c(Colors.HEADER, '━━━ 交互日志 ━━━')}")
    for i, entry in enumerate(logs, 1):
        status_icon = "✅" if entry["status"] == "ok" else "❌"
        print(f"  {c(Colors.DIM, '#%d') % i} {status_icon} [{entry['skill']}] {entry['input'][:60]}")
        summary_snippet = entry['summary'][:80] if entry['summary'] else ''
        dur = entry["duration_s"]
        print(f"    {c(Colors.DIM, f'耗时: {dur:.3f}s  |  {summary_snippet}')}")
    print(f"  {c(Colors.HEADER, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}\n")


# ── 交互模式 ───────────────────────────────────────────────────────


def interactive_mode(engine: SkillEngine) -> None:
    """REPL 交互模式"""
    print(BANNER)
    print(f"  {c(Colors.GREEN, '欢迎使用量子计算 Agent!')}")
    print(f"  输入 {c(Colors.YELLOW, 'help')} 查看可用技能，{c(Colors.YELLOW, 'logs')} 查看交互日志，")
    print(f"  {c(Colors.YELLOW, 'exit')} 或 {c(Colors.YELLOW, 'quit')} / {c(Colors.YELLOW, 'Ctrl+D')} 退出。\n")

    while True:
        try:
            user_input = input(f"  {c(Colors.CYAN, '量子Agent')} {c(Colors.DIM, '> ')}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "q"):
            break

        if user_input.lower() in ("logs", "log"):
            display_logs(engine)
            continue

        if user_input.lower() in ("clear", "cls"):
            # 清屏
            print("\033[2J\033[H", end="")
            print(BANNER)
            continue

        # 调度
        result = engine.dispatch(user_input)

        # 渲染输出
        print(render_result(result))

    # 退出前显示日志摘要
    logs = engine.get_logs()
    if logs:
        print(f"\n  {c(Colors.DIM, f'本次会话共 {len(logs)} 条交互记录')}")
        log_file = _save_session_logs(logs)
        print(f"  {c(Colors.DIM, f'日志已保存: {log_file}')}\n")

    print(f"  {c(Colors.GREEN, '再见! 👋')}\n")


# ── 单次执行模式 ───────────────────────────────────────────────────


def once_mode(engine: SkillEngine, command: str, json_output: bool = False) -> NoReturn:
    """单次执行模式"""
    result = engine.dispatch(command)

    if json_output:
        output = {
            "skill": result.skill,
            "status": result.status,
            "summary": result.summary,
            "duration_s": result.duration_s,
            "visualization": result.visualization,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(render_result(result))

    sys.exit(0 if result.status == "ok" else 1)


# ── 批量模式 ───────────────────────────────────────────────────────


def batch_mode(engine: SkillEngine, commands_file: str) -> None:
    """从文件读取命令批量执行"""
    path = Path(commands_file)
    if not path.exists():
        print(f"  {c(Colors.RED, f'文件不存在: {commands_file}')}")
        sys.exit(1)

    commands = path.read_text().strip().splitlines()
    commands = [c.strip() for c in commands if c.strip() and not c.startswith("#")]

    print(f"  {c(Colors.CYAN, f'批量执行 {len(commands)} 条命令...')}\n")

    for i, cmd in enumerate(commands, 1):
        print(f"  {c(Colors.DIM, f'[{i}/{len(commands)}]')} {c(Colors.BOLD, cmd)}")
        result = engine.dispatch(cmd)
        print(render_result(result))

    # 汇总
    logs = engine.get_logs()
    ok_count = sum(1 for l in logs if l["status"] == "ok")
    print(f"  {c(Colors.GREEN, f'完成: {ok_count}/{len(commands)} 成功')}")
    log_file = _save_session_logs(logs)
    print(f"  {c(Colors.DIM, f'日志已保存: {log_file}')}")


# ── 日志保存 ───────────────────────────────────────────────────────


def _save_session_logs(logs: list[dict]) -> str:
    """将会话日志保存到文件并返回路径"""
    log_dir = Path("agent/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"session_{timestamp}.jsonl"
    log_path.write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in logs) + "\n"
    )
    return str(log_path)


# ── 测试模式（全量演算） ──────────────────────────────────────────


def run_all_demos(engine: SkillEngine, devices: list[str] | None = None) -> None:
    """运行所有演示并输出摘要"""
    demos = [
        ("Bell态演示", "bell_state"),
        ("Grover搜索（目标态101）", "grover_search 目标态 101"),
        ("VQC变分量子分类（1层，2epoch）", "vqc_classify layers=1 epochs=2"),
        ("平流方程模拟", "advection_sim"),
        ("自定义线路（H+CNOT）", "h(0), cx(0,1)"),
        ("帮助信息", "help"),
    ]

    print(f"\n  {c(Colors.HEADER, '📋 全量算法测试报告')}")
    print(f"  {c(Colors.HEADER, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}")

    results = []
    for name, cmd in demos:
        print(f"\n  {c(Colors.CYAN, f'▶ {name}')}")
        result = engine.dispatch(cmd)
        status_icon = "✅" if result.status == "ok" else "❌"
        print(f"  {status_icon} 状态: {result.status}  |  耗时: {result.duration_s:.3f}s")
        results.append({
            "demo": name,
            "command": cmd,
            "status": result.status,
            "duration_s": result.duration_s,
        })

    # 汇总
    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"\n  {c(Colors.HEADER, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}")
    print(f"  {c(Colors.GREEN, f'📊 汇总: {ok_count}/{len(results)} 通过')}")

    # 保存报告
    report_path = Path("quantum/results/agent_test_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False)
    )
    print(f"  {c(Colors.DIM, f'报告已保存: {report_path}')}")

    # 保存交互日志
    logs = engine.get_logs()
    log_file = _save_session_logs(logs)
    print(f"  {c(Colors.DIM, f'交互日志已保存: {log_file}')}")


# ── CLI ────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="量子计算 Agent — 自然语言交互的统一演示平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python -m agent.cli                          # 交互模式\n"
            "  python -m agent.cli -c 'Bell态演示'          # 单次执行\n"
            "  python -m agent.cli -c 'Bell态演示' --json   # JSON 输出\n"
            "  python -m agent.cli -f commands.txt          # 批量执行\n"
            "  python -m agent.cli --test-all               # 全量测试\n"
        ),
    )
    parser.add_argument("-c", "--command", help="单次执行命令")
    parser.add_argument("--json", action="store_true", help="JSON 输出模式")
    parser.add_argument("-f", "--file", help="批量执行命令文件（每行一条）")
    parser.add_argument("--test-all", action="store_true", help="运行全部演示并生成测试报告")
    parser.add_argument("--no-color", action="store_true", help="禁用颜色输出")

    args = parser.parse_args()

    # 颜色支持检测
    if args.no_color or not sys.stdout.isatty():
        from types import SimpleNamespace
        dummy = SimpleNamespace()
        for a in ("HEADER", "GREEN", "YELLOW", "RED", "CYAN", "MAGENTA", "RESET", "BOLD", "DIM"):
            setattr(dummy, a, "")
        for a in ("c",):
            setattr(dummy, a, lambda color, text: text)
        global Colors
        Colors = dummy  # type: ignore

    engine = get_engine()

    if args.test_all:
        run_all_demos(engine)
    elif args.command:
        once_mode(engine, args.command, json_output=args.json)
    elif args.file:
        batch_mode(engine, args.file)
    else:
        interactive_mode(engine)


if __name__ == "__main__":
    main()