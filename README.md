# ⚛️ 量子计算模拟与算法演示平台

> **壁仞飞翔杯·量子计算 — 赛题一**  
> 基于 UnitaryLab + 壁仞 BIRENSUPA 的量子计算模拟与算法演示平台，集成 AI Agent/Skills 智能化能力，支持通过自然语言完成量子线路构建、模拟执行、结果分析与可视化展示全流程。

---

## 📋 目录

- [项目概述](#项目概述)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [Agent/Skills 系统](#agentskills-系统)
- [量子算法演示](#量子算法演示)
- [GPU 加速](#gpu-加速)
- [正确性验证](#正确性验证)
- [提交物清单](#提交物清单)
- [开发环境](#开发环境)

---

## 🚀 项目概述

本项目面向**壁仞飞翔杯·量子计算**赛题一「量子计算模拟与算法演示平台」，构建了一个集成 Agent/Skills 能力的量子计算模拟与算法演示平台。用户可通过自然语言与 AI Agent 交互，完成以下全流程任务：

1. **量子线路构建** — 支持典型量子线路和自定义线路
2. **算法配置与模拟执行** — 在 CPU/壁仞 GPU 上执行量子模拟
3. **结果分析与验证** — 自动对比 CPU 与 GPU 结果，解析验证
4. **可视化展示** — 概率分布图、线路图、训练曲线

---

## 🛠️ 技术栈

| 层 | 技术 |
|---|---|
| 量子计算框架 | [UnitaryLab](https://pypi.org/project/unitarylab/)（模拟器+算法库） |
| GPU 平台 | 壁仞 BIRENSUPA（brcc 编译器, SUPA 语言）— **8 × 32GB 壁仞 GPU** |
| AI Agent | SkillEngine — 自然语言交互调度引擎 |
| 数值验证 | SUPA GEMV 基准测试 + PyTorch 扩展 |
| 可视化 | Matplotlib（概率分布图、训练曲线） |
| 演示平台 | CLI（REPL 交互式） + Web（Flask REST API） |
| 构建工具 | Makefile（壁仞 SUPA 项目）、build.sh（PyTorch 扩展） |

---

## 📁 项目结构

```
AI-Agent-for-Quantum-Computing/
├── README.md                 # 本文件
├── CLAUDE.md                 # 项目系统提示 / 详细使用说明
├── skill.md                  # Agent/Skills 能力定义文件（提交物）
├── submission_checklist.md   # 提交物清单核查报告
├── .gitignore
│
├── quantum/
│   ├── examples/             # 量子算法演示脚本
│   │   ├── bell_state_demo.py           # Bell态制备与测量
│   │   ├── grover_demo.py               # Grover 搜索算法
│   │   ├── vqc_demo.py                  # 变分量子分类器
│   │   ├── advection_demo.py            # 平流方程（薛定谔化方法）
│   │   ├── compare_supa_unitarylab.py   # 壁仞 GPU vs UnitaryLab 交叉验证
│   │   └── supa/
│   │       └── quantum_reference.su     # 壁仞 GPU 原生量子参考实现
│   └── results/              # 运行结果（JSON、SVG 线路图）
│       ├── fundamental_algorithm/grover/
│       └── schrodingerization/equation_advection/
│
├── agent/                    # Agent/Skills 系统
│   ├── cli.py                # CLI 交互平台（REPL + 批量 + 全量测试）
│   ├── web.py                # Web 演示平台（Flask）
│   ├── demo_commands.txt     # 演示命令集
│   ├── logs/                 # 交互日志（≥5段有效记录）
│   └── skills/               # 量子计算 Skills 定义
│       ├── __init__.py       # SkillEngine — 注册与调度引擎
│       ├── bell_state.py     # Bell态制备与测量
│       ├── grover_search.py  # Grover 搜索算法
│       ├── vqc_classify.py   # VQC 变分量子分类
│       ├── advection_sim.py  # 平流方程量子模拟
│       ├── compare_backends.py # SUPA vs UnitaryLab 对比
│       ├── circuit_builder.py # 自定义量子线路
│       ├── visualize.py      # 结果可视化
│       └── help.py           # 帮助信息
│
├── ai4s/gemv/                # SUPA GEMV 内核 + PyTorch 扩展（GPU 加速示例）
│   ├── kernel/
│   │   ├── gemv.su           # SUPA 设备端 kernel
│   │   ├── test_gemv.cpp     # 精度+性能测试
│   ├── torch_extension/      # PyTorch 绑定（gemv_supa_ext）
│   └── include/              # 公用头文件
│
├── docs/                     # 壁仞 BIRENSUPA 开发文档
│   ├── 1_Software_Installation_Guide/
│   ├── 2_BIRENSUPA_Programming/
│   └── 3_Acceleration_Library/
│
└── 赛题/                     # 竞赛题目描述
    ├── README.md
    ├── 赛题一 量子计算模拟与算法演示平台.md
    └── 赛题二 量子应用与跨界探索.md
```

---

## ⚡ 快速开始

### 环境要求

```bash
# Python 3.8+
pip install unitarylab flask matplotlib
```

### 运行量子演示

```bash
cd quantum/examples

# Bell态制备与测量
python bell_state_demo.py

# Grover 搜索算法（目标态 101）
python grover_demo.py

# 变分量子分类器
python vqc_demo.py

# 平流方程（薛定谔化方法）
python advection_demo.py
```

### Agent CLI 交互平台

```bash
# 交互模式（REPL）
python -m agent.cli

# 单次执行
python -m agent.cli -c "Bell态演示"
python -m agent.cli -c "Grover搜索，目标态 101"

# JSON 输出
python -m agent.cli -c "Bell态演示" --json

# 批量执行
python -m agent.cli -f agent/demo_commands.txt

# 全量测试（运行所有演示并生成报告）
python -m agent.cli --test-all

# 输出示例:
#   📊 汇总: 6/6 通过
```

### Agent Web 演示平台

```bash
pip install flask
python -m agent.web
# 浏览器访问 http://localhost:5000
```

**Web API 端点：**

| 方法 | 端点 | 说明 |
|---|---|---|
| GET | `/` | Web 聊天界面 |
| POST | `/api/chat` | 自然语言交互（`{"text": "Bell态演示"}`） |
| GET | `/api/skills` | 列出可用技能 |
| GET | `/api/logs` | 查看交互日志 |

### SUPA GPU 项目（需要壁仞 SDK）

```bash
cd ai4s/gemv

# 编译 GEMV 内核
make build

# 精度测试
make run-accuracy

# 性能测试
make run-perf
```

### PyTorch 扩展（需要壁仞 SDK + PyTorch）

```bash
cd ai4s/gemv/torch_extension
bash build.sh
python test_gemv_ext.py
```

---

## 🤖 Agent/Skills 系统

### 技能调度流程

```
用户自然语言输入
    ↓
SkillEngine._nlu_match() — 关键词匹配 + 参数提取
    ↓
SkillSpec.handler(args)  — 执行对应技能
    ↓
自动记录日志 → agent/logs/
    ↓
返回标准格式结果（状态 / 摘要 / 可视化路径）
```

### 可用技能

| 技能 ID | 名称 | 自然语言触发 |
|---|---|---|
| `bell_state` | Bell态制备与测量 | "Bell态演示", "纠缠态" |
| `grover_search` | Grover搜索算法 | "Grover搜索", "搜索目标态 101" |
| `vqc_classify` | VQC变分量子分类 | "训练VQC，2层，5个epoch" |
| `advection_sim` | 平流方程量子模拟 | "平流方程模拟", "薛定谔化" |
| `compare_backends` | SUPA vs UnitaryLab对比 | "对比SUPA", "交叉验证" |
| `circuit_builder` | 自定义量子线路 | "h(0), cx(0,1)" |
| `visualize` | 结果可视化 | "可视化", "画图" |
| `help` | 帮助信息 | "help", "可用技能" |

### 技能定义

完整的技能定义详见 [`skill.md`](./skill.md)，每个技能包含：
- 自然语言触发示例
- 任务流程（分步骤）
- 调用链路图
- 输入输出格式（JSON Schema）
- 交互示例

### 交互日志

每次技能调用自动记录到 `agent/logs/session_<时间戳>.jsonl`：

```json
{
  "timestamp": "2026-07-19T14:57:18+00:00",
  "input": "Bell态演示",
  "skill": "bell_state",
  "status": "ok",
  "summary": "Bell态制备完成\n  |00⟩: 50.00%\n  |11⟩: 50.00%\n  ✅ CPU与GPU结果一致",
  "duration_s": 4.62
}
```

---

## 🧪 量子算法演示

### 已实现的算法

| 算法 | 状态 | 验证方式 |
|---|---|---|
| **Bell 态制备** | ✅ 已完成 | CPU vs GPU 概率对比（误差 0.0） |
| **Grover 搜索** | ✅ 已完成 | 目标态概率 0.9453，与解析值 0.9453 一致 |
| **VQC（变分量子分类器）** | ✅ 已完成 | GPU 上的 QML 训练，Iris 数据集 |
| **平流方程（薛定谔化）** | ✅ 已完成 | nx=4, na=8, T=1, 数值模拟 |
| **SUPA 参考对比** | ✅ 已完成 | 壁仞 GPU 原生 vs UnitaryLab 交叉验证（误差 < 1e-6） |
| **GEMV 加速** | ✅ 已完成 | 壁仞 GPU kernel + PyTorch 扩展（精度 3/3 通过） |

### 全量测试结果

```json
[
  { "demo": "Bell态演示",                "status": "ok", "duration_s": 4.70 },
  { "demo": "Grover搜索（目标态101）",   "status": "ok", "duration_s": 0.84 },
  { "demo": "VQC变分量子分类",           "status": "ok", "duration_s": 11.21 },
  { "demo": "平流方程模拟",               "status": "ok", "duration_s": 0.97 },
  { "demo": "自定义线路（H+CNOT）",       "status": "ok", "duration_s": 0.004 },
  { "demo": "帮助信息",                   "status": "ok", "duration_s": 0.0  }
]
```

---

## 🚀 GPU 加速

### 壁仞 GPU 配置

| 项目 | 规格 |
|---|---|
| GPU 型号 | 壁仞科技 Biren（PCI ID: `1ee0:000f`） |
| GPU 数量 | **8 张** |
| 单卡显存 | 32 GB |
| 总显存 | **256 GB** |
| SDK 版本 | BIRENSUPA 1.11.0.0.rc2 |
| 编译器 | brcc-1（基于 clang，支持 SUPA 语言） |
| 加速库 | succl（类 CUDA）、sublas、sudnn、sufft、surand |

### GEMV 性能

```
Benchmark: 4096 × 1024
  SUPA kernel (壁仞 GPU):    386 μs
  PyTorch extension (壁仞):  2.94 ms
  精度测试: 3/3 passed
```

---

## ✅ 正确性验证

| 验证项 | 方法 | 结果 |
|---|---|---|
| Bell态 | CPU vs GPU 概率对比 | 最大误差 **0.0** |
| Grover | 目标概率 vs 解析公式 | **0.9453 ≈ 0.9453** |
| SUPA 对比 | 壁仞 GPU vs UnitaryLab | Bell 误差 **2.98e-08**, Grover 误差 **5.96e-07** |
| GEMV | 3 组矩阵形状精度测试 | **全部通过** |
| GEMV 扩展 | 6 项测试（精度+错误处理+性能） | **全部通过** |

---

## 📦 提交物清单

| # | 提交物 | 状态 | 位置 |
|---|---|---|---|
| 1 | `skill.md` — Agent/Skills 能力定义文件 | ✅ | `skill.md` |
| 2 | 项目源码 | ✅ | `quantum/examples/` + `agent/skills/` + `ai4s/gemv/` |
| 3 | 依赖说明与运行命令 | ✅ | `README.md` + `CLAUDE.md` |
| 4 | 正确性验证结果 | ✅ | `quantum/results/agent_test_report.json` |
| 5 | 运行结果文件 | ✅ | JSON + SVG 线路图 + TXT |
| 6 | Agent 交互日志（≥5段） | ✅ | `agent/logs/`（45个文件, 91条记录） |
| 7 | 统一演示平台 | ✅ | CLI (`agent/cli.py`) + Web (`agent/web.py`) |
| 8 | 展示材料（PPT/视频） | 🟡 可选 | 未准备 |

---

## 💻 开发环境

```bash
# 必选
Python >= 3.8
unitarylab          # pip install unitarylab
matplotlib          # pip install matplotlib

# 可选（Web 平台）
flask               # pip install flask

# 可选（壁仞 GPU 加速）
birensupa SDK 1.11+ # 壁仞 BIRENSUPA 开发套件
torch_br            # 壁仞 PyTorch 扩展
```

---

## 📜 许可证

本项目为壁仞飞翔杯·量子计算竞赛参赛作品。

---

## 🙏 致谢

- [UnitaryLab](https://github.com/unitarylab) — 量子计算能力库与算法库
- 壁仞科技 — BIRENSUPA GPU 平台与 SDK
- 上海人工智能实验室 — 赛事组织