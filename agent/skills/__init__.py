"""
Agent/Skills 系统核心 — Skills 注册与调度引擎

提供技能注册、自然语言调度、任务执行与日志记录的框架。
每个 Skill 是一个可调用对象，接收参数字典，返回标准结果字典。
"""

from __future__ import annotations

import importlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# ── 日志目录 ──────────────────────────────────────────────────────
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ── 数据结构 ───────────────────────────────────────────────────────


@dataclass
class SkillSpec:
    """单个技能的规范定义"""
    id: str
    name: str
    description: str
    handler: Callable[..., dict]
    default_args: dict = field(default_factory=dict)


@dataclass
class SkillResult:
    """技能执行的标准返回"""
    skill: str
    status: str  # "ok" | "error" | "env_unavailable"
    summary: str
    results: dict = field(default_factory=dict)
    visualization: str | None = None
    duration_s: float = 0.0
    raw: str = ""


# ── 引擎 ───────────────────────────────────────────────────────────


class SkillEngine:
    """技能注册与调度引擎"""

    def __init__(self):
        self._skills: dict[str, SkillSpec] = {}
        self._session_log: list[dict] = []
        self._init_builtin_skills()

    # ── 注册 ──

    def register(self, spec: SkillSpec) -> None:
        self._skills[spec.id] = spec

    def _init_builtin_skills(self) -> None:
        """注册内置技能（懒加载 handler，避免 import 循环）"""
        builtins = [
            SkillSpec("bell_state", "Bell态制备与测量",
                       "构建2量子比特Bell态，展示纠缠态概率分布",
                       self._lazy_handler("bell_state")),
            SkillSpec("grover_search", "Grover搜索算法",
                       "3量子比特无结构搜索，放大目标态概率",
                       self._lazy_handler("grover_search")),
            SkillSpec("vqc_classify", "VQC变分量子分类",
                       "变分量子线路二分类训练与评估",
                       self._lazy_handler("vqc_classify")),
            SkillSpec("advection_sim", "平流方程量子模拟",
                       "薛定谔化方法求解一维平流方程",
                       self._lazy_handler("advection_sim")),
            SkillSpec("compare_backends", "SUPA vs UnitaryLab对比",
                       "壁仞GPU原生实现与UnitaryLab交叉验证",
                       self._lazy_handler("compare_backends")),
            SkillSpec("circuit_builder", "自定义量子线路",
                       "从自然语言描述构建任意量子线路并执行",
                       self._lazy_handler("circuit_builder")),
            SkillSpec("visualize", "结果可视化",
                       "将运行结果绘制为概率分布图或线路图",
                       self._lazy_handler("visualize")),
            SkillSpec("help", "帮助信息",
                       "列出所有可用技能及其描述",
                       self._help_handler),
            SkillSpec("list_skills", "列出技能",
                       "展示所有已注册的技能",
                       self._list_skills_handler),
        ]
        for s in builtins:
            self._skills[s.id] = s

    @staticmethod
    def _lazy_handler(skill_id: str) -> Callable:
        def _handler(args: dict) -> dict:
            mod = importlib.import_module(f"agent.skills.{skill_id}")
            return mod.run(args)
        return _handler

    # ── 调度 ──

    def dispatch(self, text: str) -> SkillResult:
        """自然语言 → 技能调度"""
        text = text.strip()

        # 1. 精确匹配技能名
        if text.lower() in self._skills:
            skill_id = text.lower()
            args = {}
        else:
            # 2. 关键词匹配
            skill_id, args = self._nlu_match(text)

        spec = self._skills.get(skill_id)
        if spec is None:
            return SkillResult(
                skill="unknown",
                status="error",
                summary=f"未能识别您的意图。可用技能：{', '.join(self._skills.keys())}。输入 help 查看详情。",
            )

        # 合并默认参数
        merged_args = {**spec.default_args, **args}

        # 执行
        t0 = time.perf_counter()
        try:
            raw_result = spec.handler(merged_args)
            status = raw_result.get("status", "ok")
            summary = raw_result.get("summary", f"{spec.name} 执行完成")
            vis = raw_result.get("visualization")
            duration = time.perf_counter() - t0
            result = SkillResult(
                skill=skill_id,
                status=status,
                summary=summary,
                results=raw_result.get("results", raw_result),
                visualization=vis,
                duration_s=round(duration, 3),
                raw=json.dumps(raw_result, ensure_ascii=False, indent=2),
            )
        except Exception as e:
            duration = time.perf_counter() - t0
            result = SkillResult(
                skill=skill_id,
                status="error",
                summary=f"执行失败: {e}",
                duration_s=round(duration, 3),
            )

        # 记录日志
        self._log(text, result)
        return result

    def _nlu_match(self, text: str) -> tuple[str, dict]:
        """简单的基于关键词的自然语言理解"""
        text_lower = text.lower()
        # 保存原始输入用于参数传递（所有技能）
        args: dict[str, Any] = {"text": text, "gates": text, "input": text}

        # 提取 device
        if "gpu" in text_lower or ("device" in text_lower and "gpu" in text_lower):
            args["device"] = "gpu"
        elif "cpu" in text_lower:
            args["device"] = "cpu"

        # 提取目标态 (Grover)
        m = re.search(r'(?:目标态|target|搜索)\s*[:：]?\s*([01]+)', text)
        if m:
            args["target"] = m.group(1)

        # 提取层数 (VQC)
        m = re.search(r'(\d+)\s*(?:层|l(?:ayer)?s?)', text_lower)
        if m:
            args["layers"] = int(m.group(1))

        # 提取 epoch
        m = re.search(r'(\d+)\s*(?:epoch|轮|次)', text_lower)
        if m:
            args["epochs"] = int(m.group(1))

        # 提取学习率
        m = re.search(r'lr[\s=:]+([\d.]+)', text_lower)
        if m:
            args["lr"] = float(m.group(1))

        # 关键词 -> skill
        keyword_map = [
            (["bell", "纠缠", "entangle"], "bell_state"),
            (["grover", "搜索", "search"], "grover_search"),
            (["vqc", "变分", "分类", "classif"], "vqc_classify"),
            (["平流", "advection", "薛定谔化", "方程"], "advection_sim"),
            (["对比", "compare", "cross", "supa", "backend", "验证"], "compare_backends"),
            (["自定义", "custom", "线路", "circuit"], "circuit_builder"),
            (["可视化", "visual", "图", "plot", "chart", "画"], "visualize"),
            (["帮助", "help", "技能", "skill", "可用"], "help"),
        ]
        for keywords, skill_id in keyword_map:
            if any(kw in text_lower for kw in keywords):
                return skill_id, args

        # 保存原始输入用于参数传递
        args["_raw_input"] = text

        # 检查是否有自定义线路语法
        if re.search(r'(?:h\(|x\(|cx\(|rx\(|ry\(|rz\(|H\s+\d)', text_lower):
            return "circuit_builder", args

        return "help", args

    # ── 内置 handler ──

    @staticmethod
    def _help_handler(args: dict) -> dict:
        from agent.skills import help as help_mod
        return help_mod.run(args)

    @staticmethod
    def _list_skills_handler(args: dict) -> dict:
        skills_list = [
            {"id": "help", "name": "帮助信息"},
            {"id": "bell_state", "name": "Bell态制备与测量"},
            {"id": "grover_search", "name": "Grover搜索算法"},
            {"id": "vqc_classify", "name": "VQC变分量子分类"},
            {"id": "advection_sim", "name": "平流方程量子模拟"},
            {"id": "compare_backends", "name": "SUPA vs UnitaryLab对比"},
            {"id": "circuit_builder", "name": "自定义量子线路"},
            {"id": "visualize", "name": "结果可视化"},
        ]
        return {
            "status": "ok",
            "summary": "可用技能：" + ", ".join(s["name"] for s in skills_list),
            "results": {"skills": skills_list},
        }

    # ── 日志 ──

    def _log(self, user_input: str, result: SkillResult) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": user_input,
            "skill": result.skill,
            "status": result.status,
            "summary": result.summary,
            "duration_s": result.duration_s,
        }
        self._session_log.append(entry)
        log_path = LOGS_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(log_path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_logs(self) -> list[dict]:
        return self._session_log

    def list_skills(self) -> list[dict]:
        return [
            {"id": s.id, "name": s.name, "description": s.description}
            for s in self._skills.values()
        ]


# ── 全局单例 ───────────────────────────────────────────────────────

_engine: SkillEngine | None = None


def get_engine() -> SkillEngine:
    global _engine
    if _engine is None:
        _engine = SkillEngine()
    return _engine