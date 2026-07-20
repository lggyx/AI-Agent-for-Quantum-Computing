# 提交物清单 — 量子计算模拟与算法演示平台

> 赛题一 · 壁仞飞翔杯·量子计算
> 最后验证时间: 2026-07-21
> 最后一次全量测试: ✅ 6/6 通过

---

## ✅ 全部通过 — 6 项提交物核查结果

### 1. skill.md 文件（必须提交）
| 文件 | 大小 | 状态 |
|---|---|---|
| `skill.md` | 8,389 B | ✅ 已提交 (a88ca68) |

**内容概要**: 定义 7 个量子计算技能 + 帮助技能，包含技能触发方式、任务流程、调用链路、输入输出格式及自然语言交互示例。

---

### 2. 项目源码

| 分类 | 文件 | 说明 |
|---|---|---|
| **量子算法演示** | `quantum/examples/bell_state_demo.py` | Bell态制备与测量 |
| | `quantum/examples/grover_demo.py` | Grover搜索算法 |
| | `quantum/examples/vqc_demo.py` | VQC变分量子分类 |
| | `quantum/examples/advection_demo.py` | 平流方程（薛定谔化） |
| | `quantum/examples/compare_supa_unitarylab.py` | SUPA vs UnitaryLab对比 |
| **GPU 加速** | `ai4s/gemv/kernel/gemv.su` | SUPA 设备端 kernel |
| | `ai4s/gemv/torch_extension/gemv_supa_ext.cpp` | PyTorch 绑定 |
| **Agent/Skills** | `agent/skills/__init__.py` | 技能注册与调度引擎 |
| | `agent/skills/bell_state.py` | Bell态技能（含SVG线路图） |
| | `agent/skills/grover_search.py` | Grover搜索技能 |
| | `agent/skills/vqc_classify.py` | VQC分类技能（GPU加速，默认2层10epoch） |
| | `agent/skills/advection_sim.py` | 平流方程技能 |
| | `agent/skills/compare_backends.py` | 后端对比技能 |
| | `agent/skills/circuit_builder.py` | 自定义线路技能 |
| | `agent/skills/visualize.py` | 可视化技能 |
| | `agent/skills/help.py` | 帮助技能 |
| **演示平台** | `agent/cli.py` | CLI 交互平台（REPL/单次/批量/全量测试） |
| | `agent/web.py` | Web 演示平台（Flask，优化UI，图片预览） |

---

### 3. 依赖说明与运行命令
✅ 完整记录在 `CLAUDE.md` 中，涵盖:
- Python 量子演示运行命令
- Agent CLI 交互平台（REPL / 单次 / 批量 / 全量测试）
- Agent Web 演示平台（Flask，支持可视化图片内嵌预览）
- SUPA GPU 项目构建（需壁仞 SDK）
- PyTorch 扩展编译（需壁仞 SDK）

---

### 4. 正确性验证
✅ **全量测试: 6/6 通过** (最近一次: 2026-07-21)

| 测试项 | 结果 | 耗时 |
|---|---|---|
| Bell态制备（含SVG线路图 + 概率分布图） | ✅ ok | ~4.8s |
| Grover搜索（目标态101，概率 0.9453） | ✅ ok (理论验证，3轮迭代) | ~0.8s |
| VQC变分量子分类（GPU加速，默认2层10epoch） | ✅ ok (准确率最高 **73.33%**) | ~12s (1层1epoch) / ~209s (2层10epoch) |
| 平流方程模拟（薛定谔化法） | ✅ ok (nx=4, na=8, T=1) | ~1.0s |
| 自定义线路 H+CNOT | ✅ ok | <0.1s |
| 帮助信息 | ✅ ok | <0.1s |

**验证报告**: `quantum/results/agent_test_report.json`

**VQC 参数调优结果（壁仞 GPU 加速）**:

| 配置 | 准确率 | 量子计算耗时 | 说明 |
|---|---|---|---|
| layers=1, epochs=1 (旧默认) | 66.67% | 12.6s | 原始参数 |
| **layers=2, epochs=10, lr=0.01 (GPU)** | **73.33%** ✅ | 207.6s | **最佳精度**，壁仞GPU加速 |

---

### 5. 运行结果文件

| 文件 | 类型 |
|---|---|
| `quantum/results/agent_test_report.json` | Agent 全量测试报告 |
| `quantum/results/fundamental_algorithm/grover/grover_algorithm_circuit.svg` | Grover 线路图 |
| `quantum/results/fundamental_algorithm/grover/grover_algorithm_result.txt` | Grover 运行结果 |
| `quantum/results/schrodingerization/equation_advection/1D_Advection_Classical_nx=4_na=8_T=1_circuit_full.svg` | 平流方程线路图 |
| `quantum/results/schrodingerization/equation_advection/1D_Advection_Classical_nx=4_na=8_T=1_solution.svg` | 平流方程数值解图 |
| `quantum/results/plots/bell_state_probs.png` | Bell态概率分布图 |
| `quantum/results/plots/bell_state_circuit.svg` | Bell态线路图（手绘SVG） |

---

### 6. Agent 交互日志（至少 5 段有效记录）
✅ **大量记录** 保存在 `agent/logs/` 目录

日志文件示例: `session_20260720_161744.jsonl`（最近一次全量测试日志，6条交互）

---

## 📊 提交物总检查表

| # | 提交物 | 状态 | 备注 |
|---|---|---|---|
| 1 | `skill.md` | ✅ | 7技能定义 + 交互协议（已更新默认参数） |
| 2 | 项目源码 | ✅ | 演示 + GPU加速 + Agent系统 |
| 3 | 依赖说明与运行命令 | ✅ | CLAUDE.md |
| 4 | 正确性验证结果 | ✅ | 6/6 通过，含理论验证 |
| 5 | 运行结果文件 | ✅ | JSON + SVG + PNG + TXT |
| 6 | Agent 交互日志 (≥5段) | ✅ | >60条记录 |
| 7 | DEMO 平台 (CLI/Web) | ✅ | `agent/cli.py` + `agent/web.py`（优化UI+图片预览）|
| 8 | 展示材料 (PPT/视频) | 🟡 可选 | 未准备 |

---

## ⚡ GPU 加速能力

| 特性 | 说明 |
|---|---|
| 模拟后端 | UnitaryLab GPU 后端（基于壁仞 torch_br） |
| GPU 框架 | PyTorch + torch_br (torch_br 1.10.0.20900+br1xx) |
| 加速算法 | Bell态、Grover搜索、VQC训练、平流方程 |
| 交叉验证 | CPU vs GPU 结果一致（Bell态误差 < 1e-5） |
| SUPA 原生 | GEMV 内核 (ai4s/gemv) + PyTorch 扩展（需brcc编译） |

---

## 🚀 运行方式

```bash
# 1. 安装依赖
pip install unitarylab flask

# 2. 全量测试（6项算法验证）
python -m agent.cli --test-all

# 3. CLI 交互模式
python -m agent.cli

# 4. Web 演示平台（优化版UI，支持图片内嵌预览）
python -m agent.web
# 浏览器打开 http://localhost:5000
```