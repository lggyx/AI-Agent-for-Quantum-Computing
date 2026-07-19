# CLAUDE.md — AI Agent for Quantum Computing

## 项目概述

本项目面向 **壁仞飞翔杯·量子计算** 赛题一「量子计算模拟与算法演示平台」，构建一个集成 Agent/Skills 能力的量子计算模拟与算法演示平台。用户可通过自然语言与 AI Agent 交互，完成量子线路构建、模拟执行、结果分析与可视化展示等全流程任务。

## 技术栈

| 层 | 技术 |
|---|---|
| 量子计算框架 | [UnitaryLab](https://pypi.org/project/unitarylab/)（模拟器+算法库） |
| GPU 平台 | 壁仞 BIRENSUPA（brcc 编译器, SUPA 语言） |
| AI Agent | Claude Code + Skills（自然语言交互） |
| 数值验证 | SUPA GEMV 基准测试 + PyTorch 扩展 |
| 可视化 | Matplotlib / Plotly（线路图、概率分布、误差分析） |
| 构建工具 | Makefile（壁仞 SUPA 项目）、Python（量子演示） |

## 项目结构

```
AI-Agent-for-Quantum-Computing/
├── CLAUDE.md               # 项目系统提示 / 使用说明
├── skill.md                # Agent/Skills 能力定义文件（提交物）
├── .gitignore
├── ai4s/gemv/              # SUPA GEMV 内核 + PyTorch 扩展（GPU 加速示例）
│   ├── kernel/gemv.su      # SUPA 设备端 kernel
│   ├── kernel/test_gemv.cpp # 精度+性能测试
│   ├── torch_extension/    # PyTorch 绑定（gemv_supa_ext）
│   └── include/            # 公用头文件（DeviceBuffer, 计时, 防作弊）
├── quantum/
│   ├── examples/           # 量子算法演示脚本
│   │   ├── bell_state_demo.py
│   │   ├── grover_demo.py
│   │   ├── vqc_demo.py
│   │   ├── advection_demo.py
│   │   ├── compare_supa_unitarylab.py
│   │   └── supa/quantum_reference.su  # 壁仞 GPU 原生量子参考实现
│   └── results/            # 运行结果（JSON、SVG 线路图）
├── docs/                   # 壁仞 BIRENSUPA 开发文档
│   ├── 1_Software_Installation_Guide/
│   ├── 2_BIRENSUPA_Programming/
│   └── 3_Acceleration_Library/
├── 赛题/                   # 竞赛题目描述
│   ├── README.md
│   ├── 赛题一 量子计算模拟与算法演示平台.md
│   └── 赛题二 量子应用与跨界探索.md
├── agent/                  # Agent/Skills 系统
│   ├── cli.py              # CLI 交互平台（REPL + 批量 + 全量测试）
│   ├── web.py              # Web 演示平台（Flask）
│   ├── demo_commands.txt   # 演示命令集（用于批量测试）
│   ├── logs/               # 交互日志（至少5段有效记录）
│   └── skills/             # 量子计算 Skills 定义
│       ├── __init__.py     # 注册与调度引擎
│       ├── bell_state.py
│       ├── grover_search.py
│       ├── vqc_classify.py
│       ├── advection_sim.py
│       ├── compare_backends.py
│       ├── circuit_builder.py
│       ├── visualize.py
│       └── help.py
```

## 构建与运行

### Python 量子演示（UnitaryLab）

```bash
cd quantum/examples
python bell_state_demo.py          # Bell态演示
python grover_demo.py              # Grover 搜索算法
python vqc_demo.py                 # 变分量子分类器
python advection_demo.py           # 平流方程（薛定谔化方法）
python compare_supa_unitarylab.py  # 壁仞 GPU vs UnitaryLab 交叉验证
```

### Agent CLI 交互平台

```bash
# 交互模式（REPL）
python -m agent.cli

# 单次执行
python -m agent.cli -c "Bell态演示"

# 全量测试（运行所有演示并生成报告）
python -m agent.cli --test-all

# JSON 输出模式
python -m agent.cli -c "Bell态演示" --json

# 批量执行（从文件读取命令）
python -m agent.cli -f agent/demo_commands.txt
```

### Agent Web 演示平台

```bash
pip install flask
python -m agent.web
# 浏览器访问 http://localhost:5000
```

### SUPA GPU 项目（需要壁仞 SDK）

```bash
cd ai4s/gemv
make build                         # 编译 GEMV 内核
make run-accuracy                  # 精度测试
make run-perf                      # 性能测试
```

### PyTorch 扩展（需要壁仞 SDK + PyTorch）

```bash
cd ai4s/gemv/torch_extension
bash build.sh                      # 编译 SUPA PyTorch 扩展
python test_gemv_ext.py            # 运行测试
```

## 已实现的量子算法

| 算法 | 状态 | 验证方式 |
|---|---|---|
| Bell 态制备 | ✅ 已完成 | CPU vs GPU 概率对比 |
| Grover 搜索 | ✅ 已完成 | 目标态概率 0.9453，解析验证 |
| VQC（变分量子分类器） | ✅ 已完成 | GPU 上的 QML 训练 |
| 平流方程（薛定谔化） | ✅ 已完成 | nx=4, na=8, T=1, 误差分析 |
| SUPA 参考对比 | ✅ 已完成 | 壁仞 GPU 原生 vs UnitaryLab 交叉验证 |
| GEMV 加速 | ✅ 已完成 | 壁仞 GPU kernel + PyTorch 扩展 |

## Agent/Skills 系统

### 技能调度流程

```
用户自然语言输入
    ↓
SkillEngine._nlu_match()  — 关键词匹配 + 参数提取
    ↓
SkillSpec.handler(args)   — 执行对应技能
    ↓
自动记录日志 → agent/logs/
    ↓
返回标准格式结果（状态 / 摘要 / 可视化路径）
```

### 可用技能

| 技能 ID | 名称 | 触发关键词 |
|---|---|---|
| `bell_state` | Bell态制备与测量 | bell, 纠缠, entangle |
| `grover_search` | Grover搜索算法 | grover, 搜索, search |
| `vqc_classify` | VQC变分量子分类 | vqc, 变分, 分类 |
| `advection_sim` | 平流方程量子模拟 | 平流, advection, 薛定谔化 |
| `compare_backends` | SUPA vs UnitaryLab对比 | 对比, compare, supa |
| `circuit_builder` | 自定义量子线路 | 自定义, custom, circuit |
| `visualize` | 结果可视化 | 可视化, visual, 图 |

### 交互日志

每次技能调用自动记录到 `agent/logs/session_<时间戳>.jsonl`，结构：

```json
{"timestamp": "...", "input": "Bell态演示", "skill": "bell_state",
 "status": "ok", "summary": "Bell态制备完成...", "duration_s": 4.42}
```

## 提交物清单（赛题一）

- [x] 项目源码（量子演示、GPU 加速示例）
- [x] 依赖说明与运行命令（README）
- [x] 正确性验证（Grover 解析验证、SUPA vs UnitaryLab 对比）
- [x] 运行结果（JSON、SVG 线路图）
- [x] **Agent/Skills 系统**（skill.md + 7个技能 + 引擎）
- [x] **skill.md 文件**（必须提交）
- [x] **Agent 交互日志**（至少 5 段有效记录）
- [x] **统一演示平台**（CLI REPL + Web Flask）
- [ ] **展示材料**（PPT/视频，可选但建议）

## 开发环境

- Python 3.8+
- UnitaryLab（`pip install unitarylab`）
- 壁仞 BIRENSUPA SDK（可选，用于 GPU 原生加速）
- PyTorch + torch_br（可选，用于 PyTorch SUPA 扩展）