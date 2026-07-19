# Quantum Computing Agent Skills — 量子计算智能体能力定义

## 概述

本文件定义 AI Agent 在量子计算模拟与算法演示平台中的 Skills（技能）体系。每个 Skill 封装一个完整的量子计算任务闭环，支持通过自然语言激活与执行，涵盖线路构建、算法配置、模拟执行、结果分析与可视化展示全流程。

## 技能总览

| 技能 ID | 名称 | 描述 | 输入 | 输出 |
|---|---|---|---|---|
| `bell_state` | Bell态制备与测量 | 构建2量子比特Bell态线路，展示纠缠态概率分布 | `device` (cpu/gpu) | 概率向量、线路图、验证结果 |
| `grover_search` | Grover搜索算法 | 面向3量子比特的无结构搜索，放大目标态概率 | `target` (比特串), `device` | 搜索概率、线路图、结果态 |
| `vqc_classify` | VQC变分量子分类 | 变分量子线路二分类训练与评估 | `layers`, `epochs`, `lr`, `device` | 准确率、损失曲线、训练过程 |
| `advection_sim` | 平流方程量子模拟 | 薛定谔化方法求解一维平流方程 | `nx`, `na`, `T` | 数值解、误差分析 |
| `compare_backends` | SUPA vs UnitaryLab对比 | 壁仞GPU原生实现与UnitaryLab交叉验证 | 无（使用预设参数） | 误差指标、一致性报告 |
| `circuit_builder` | 自定义量子线路 | 从自然语言描述构建任意量子线路并执行 | `qubits`, `gates` (门序列) | 状态矢量、概率分布、线路图 |
| `visualize` | 结果可视化 | 将运行结果绘制为概率分布图或线路图 | `data` (运行结果) | SVG/PNG 图表 |

## 技能详细定义

### 1. `bell_state` — Bell态制备与测量

**自然语言触发示例：**
- "运行Bell态演示"
- "制备一个2量子比特的纠缠态"
- "Bell state demo"

**任务流程：**
1. 构建 2-qubit 量子线路
2. 施加 H 门于 qubit 0
3. 施加 CNOT 门于 (0, 1)
4. 在指定设备（cpu/gpu）上执行模拟
5. 计算概率分布
6. 验证 CPU 与 GPU 结果一致性
7. 输出概率向量并保存结果

**调用链路：**
```
用户输入 → NLU解析 → skill=bell_state, args={device} → build_circuit() → execute() → analyze() → visualize() → 输出报告
```

---

### 2. `grover_search` — Grover搜索算法

**自然语言触发示例：**
- "运行Grover搜索，目标态101"
- "在3量子比特上搜索 101"
- "Grover algorithm demo"

**任务流程：**
1. 设置搜索空间（n=3）
2. 设置目标态（如 "101"）
3. 构建 Grover 线路（Oracle + 扩散算子）
4. 执行 Grover 迭代
5. 测量并计算目标态概率
6. 验证：目标态概率 ≈ 0.9453（解析值）
7. 输出搜索摘要

**调用链路：**
```
用户输入 → NLU解析 → skill=grover_search, args={target, device} → GroverAlgorithm.run() → pick_result() → verify() → 输出报告
```

---

### 3. `vqc_classify` — VQC变分量子分类

**自然语言触发示例：**
- "训练一个VQC分类器"
- "运行变分量子算法，2层，10个epoch"
- "VQC demo"

**任务流程：**
1. 初始化变分量子线路
2. 配置训练参数（层数、epochs、学习率）
3. 在GPU上执行量子-经典混合训练
4. 采集训练损失与准确率
5. 输出训练结果摘要

**调用链路：**
```
用户输入 → NLU解析 → skill=vqc_classify, args={layers, epochs, lr} → VQCAlgorithm.run() → collect_metrics() → 输出报告
```

---

### 4. `advection_sim` — 平流方程量子模拟

**自然语言触发示例：**
- "用薛定谔化方法求解平流方程"
- "运行平流方程模拟"
- "advection demo"

**任务流程：**
1. 设置空间网格（nx=4）与辅助比特数（na=8）
2. 构建薛定谔化量子线路
3. 执行时间演化（T=1）
4. 提取数值解
5. 计算误差分析
6. 输出模拟结果

**调用链路：**
```
用户输入 → NLU解析 → skill=advection_sim, args={nx, na, T} → AdvectionEquationAlgorithm.run() → simplify() → 输出报告
```

---

### 5. `compare_backends` — SUPA vs UnitaryLab对比

**自然语言触发示例：**
- "对比壁仞GPU和UnitaryLab的结果"
- "交叉验证所有算法"
- "SUPA vs UnitaryLab comparison"

**任务流程：**
1. 运行 SUPA 原生 Bell 态 + Grover（需壁仞SDK）
2. 运行 UnitaryLab 对应算法
3. 逐项对比概率/结果
4. 计算误差指标
5. 输出一致性报告

**调用链路：**
```
用户输入 → NLU解析 → skill=compare_backends → run_supa() + unitarylab_bell_probs() + unitarylab_grover() → compare() → 输出报告
```

> ⚠️ 本技能依赖壁仞 BIRENSUPA SDK，在无 SDK 环境下仅报告"环境不可用"。

---

### 6. `circuit_builder` — 自定义量子线路

**自然语言触发示例：**
- "构建一个3量子比特线路，h(0), cx(0,1), cx(1,2)"
- "创建线路: H 0, CNOT 0 1, measure all"
- "custom circuit with H and CNOT gates"

**任务流程：**
1. 解析自然语言门序列描述
2. 构造对应量子线路
3. 在指定设备上执行模拟
4. 输出状态矢量与概率分布
5. 生成线路示意图

**调用链路：**
```
用户输入 → NLU解析 → skill=circuit_builder, args={qubits, gates, device} → parse_gates() → Circuit() → execute() → analyze() → 输出报告
```

**支持的门类型：**
| 门 | 别名 | 参数 |
|---|---|---|
| H | Hadamard, h | target qubit |
| X | Pauli-X, not, x | target qubit |
| Y | Pauli-Y, y | target qubit |
| Z | Pauli-Z, z | target qubit |
| CX | CNOT, cnot, cx | control, target |
| CZ | cz | control, target |
| RX | rx | target, theta |
| RY | ry | target, theta |
| RZ | rz | target, theta |
| Measure | measure, m | target qubit |

---

### 7. `visualize` — 结果可视化

**自然语言触发示例：**
- "绘制概率分布图"
- "显示线路图"
- "可视化运行结果"

**任务流程：**
1. 读取运行结果数据
2. 根据数据类型选择图表类型（概率分布 / 线路图 / 训练曲线）
3. 使用 Matplotlib 生成图表
4. 保存为 SVG/PNG 文件
5. 返回文件路径

**支持的可视化类型：**
- 概率分布柱状图（Bell态、Grover结果等）
- 量子线路示意图（ASCII/文本形式）
- 训练损失/准确率曲线（VQC）
- 数值解对比图（平流方程）

---

## 技能调度规则

1. **匹配优先级**：精确匹配技能名 > 自然语言关键词匹配 > 默认 Fallback
2. **设备选择**：优先使用 `gpu`（CUDA 可用时），回退到 `cpu`
3. **参数默认值**：所有参数均有安全默认值，用户可部分覆盖
4. **错误处理**：执行失败时返回明确错误信息，含建议操作
5. **日志记录**：每次 Skill 调用自动记录到 `agent/logs/` 目录

## 交互协议

### 输入格式（自然语言 → 技能）

```
<自然语言描述>
```

内部解析为技能调用：

```json
{
  "skill": "<技能ID>",
  "args": { "<参数名>": "<参数值>", ... }
}
```

### 输出格式

```json
{
  "skill": "<技能ID>",
  "status": "ok | error | env_unavailable",
  "summary": "任务摘要文本",
  "results": { ... },
  "visualization": "<图表文件路径 | null>",
  "duration_s": "<执行耗时(秒)>"
}
```

## 交互示例

### 示例 1：Bell 态

**用户**：运行Bell态演示

**Agent**：
```
🧪 Bell态制备与测量
═══════════════════════════════════════
设备: cpu → gpu (自动选择)
线路: H(0), CNOT(0,1)
执行结果:
  状态 |00⟩: 50.00%
  状态 |11⟩: 50.00%
✅ CPU与GPU结果一致，最大误差 0.00
线路图: results/circuits/bell_state_circuit.svg
```

### 示例 2：Grover 搜索

**用户**：搜索目标态 101

**Agent**：
```
🔍 Grover搜索算法
═══════════════════════════════════════
搜索空间: 3 量子比特 (8 个态)
目标态: |101⟩
执行结果:
  目标态概率: 0.9453 (理论值: 0.9453)
  最概然态: |101⟩
✅ 与解析结果一致
```

### 示例 3：VQC 训练

**用户**：训练 VQC，2 层，5 个 epoch

**Agent**：
```
🧠 VQC变分量子分类器训练
═══════════════════════════════════════
训练配置: layers=2, epochs=5, lr=0.05, batch=4
训练结果:
  最终损失: 0.0234
  最终准确率: 95.83%
  量子计算时间: 0.87s
✅ 训练完成
```