"""
Quantum Agent Web — Flask 轻量版 Web 演示平台

提供 Web 界面和 REST API 两种交互方式。
优化版：增加可视化预览、快速对比、技能说明、运行状态展示。
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string, request, send_from_directory

from agent.skills import get_engine

app = Flask(__name__)
engine = get_engine()

# ── 静态文件路径 ──────────────────────────────────────────────────────

RESULTS_DIR = Path(__file__).resolve().parent.parent / "quantum" / "results"
PLOTS_DIR = RESULTS_DIR / "plots"


# ── HTML 模板 ──────────────────────────────────────────────────────

INDEX_HTML = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>量子计算 Agent 演示平台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e1a;
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container { max-width: 960px; margin: 0 auto; padding: 20px; }
        header {
            text-align: center; padding: 30px 0 20px;
            border-bottom: 1px solid #1e2a45;
        }
        header h1 {
            font-size: 1.8rem; background: linear-gradient(135deg, #6c8cff, #00d4aa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        header p { color: #8892b0; margin-top: 8px; font-size: 0.9rem; }
        .main-row { display: flex; gap: 16px; margin: 16px 0; flex-wrap: wrap; }
        .chat-col { flex: 1; min-width: 300px; }
        .info-col { flex: 0 0 280px; }
        .chat-box {
            background: #111827; border-radius: 12px;
            border: 1px solid #1e2a45; min-height: 400px; max-height: 480px;
            overflow-y: auto; padding: 16px;
        }
        /* 技能面板 */
        .skill-panel {
            background: #111827; border-radius: 12px;
            border: 1px solid #1e2a45; padding: 14px;
        }
        .skill-panel h3 {
            font-size: 0.9rem; color: #6c8cff; margin-bottom: 10px;
            border-bottom: 1px solid #1e2a45; padding-bottom: 6px;
        }
        .skill-item {
            padding: 6px 0; cursor: pointer; transition: 0.2s;
            border-bottom: 1px solid #0d1525;
        }
        .skill-item:hover { color: #00d4aa; }
        .skill-item .name { font-size: 0.85rem; font-weight: bold; }
        .skill-item .desc { font-size: 0.75rem; color: #8892b0; margin-top: 1px; }
        /* 统计卡片 */
        .stats-row { display: flex; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; }
        .stat-card {
            flex: 1; min-width: 100px; background: #0f1525; border-radius: 8px;
            border: 1px solid #1a2a44; padding: 10px; text-align: center;
        }
        .stat-card .val { font-size: 1.2rem; font-weight: bold; color: #00d4aa; }
        .stat-card .lbl { font-size: 0.7rem; color: #8892b0; margin-top: 4px; }
        /* 消息样式 */
        .msg { margin-bottom: 12px; }
        .msg-user {
            background: #1a2340; border-radius: 8px 8px 8px 0;
            padding: 10px 14px; max-width: 80%; margin-left: auto;
            border: 1px solid #2a3a5a;
        }
        .msg-agent {
            background: #0f1a2e; border-radius: 8px 8px 0 8px;
            padding: 10px 14px; max-width: 92%; margin-right: auto;
            border: 1px solid #1a2a44;
        }
        .msg-agent pre {
            white-space: pre-wrap; font-family: inherit; font-size: 0.85rem;
            line-height: 1.6; color: #c8d0e0;
        }
        .msg-label { font-size: 0.75rem; margin-bottom: 4px; font-weight: bold; }
        .msg-label.user-label { color: #00d4aa; text-align: right; }
        .msg-label.agent-label { color: #6c8cff; }
        .msg-status {
            display: inline-block; font-size: 0.7rem; padding: 1px 8px;
            border-radius: 10px; margin-left: 6px;
        }
        .msg-status.ok { background: #003d2a; color: #00d4aa; }
        .msg-status.error { background: #3d0000; color: #ff5a5a; }
        .msg-status.env_unavailable { background: #3d2a00; color: #ffaa33; }
        .msg-vis {
            margin-top: 8px; border-top: 1px solid #1e2a45; padding-top: 8px;
        }
        .msg-vis img {
            max-width: 100%; border-radius: 8px; border: 1px solid #2a3a5a;
            cursor: pointer; transition: 0.3s;
        }
        .msg-vis img:hover { border-color: #6c8cff; transform: scale(1.02); }
        .msg-vis a { color: #6c8cff; font-size: 0.8rem; text-decoration: none; }
        .msg-vis a:hover { text-decoration: underline; }
        .msg-time { font-size: 0.65rem; color: #556; margin-top: 4px; text-align: right; }
        /* 输入行 */
        .input-row {
            display: flex; gap: 8px; margin-top: 12px;
        }
        .input-row input {
            flex: 1; background: #111827; border: 1px solid #1e2a45;
            border-radius: 8px; padding: 12px 16px; color: #e0e0e0;
            font-size: 0.95rem; outline: none;
        }
        .input-row input:focus { border-color: #6c8cff; }
        .input-row button {
            background: linear-gradient(135deg, #6c8cff, #00d4aa);
            border: none; border-radius: 8px; padding: 0 24px;
            color: #fff; font-weight: bold; font-size: 0.95rem;
            cursor: pointer; transition: opacity 0.2s;
        }
        .input-row button:hover { opacity: 0.9; }
        .quick-btns {
            display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px;
        }
        .quick-btns button {
            background: #1a2340; border: 1px solid #2a3a5a; border-radius: 16px;
            padding: 6px 14px; color: #8892b0; font-size: 0.8rem; cursor: pointer;
            transition: all 0.2s;
        }
        .quick-btns button:hover { border-color: #6c8cff; color: #e0e0e0; }
        .status-bar {
            text-align: center; padding: 16px; color: #8892b0; font-size: 0.8rem;
            border-top: 1px solid #1e2a45; margin-top: 20px;
        }
        .loading { opacity: 0.5; pointer-events: none; }
        /* Scrollbar */
        .chat-box::-webkit-scrollbar { width: 4px; }
        .chat-box::-webkit-scrollbar-track { background: #0a0e1a; }
        .chat-box::-webkit-scrollbar-thumb { background: #2a3a5a; border-radius: 2px; }
        /* Modal for image */
        .modal {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); z-index: 999;
            justify-content: center; align-items: center;
        }
        .modal img { max-width: 90%; max-height: 90%; border-radius: 8px; }
        @media (max-width: 700px) { .info-col { flex: 0 0 100%; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚛ 量子计算 Agent 演示平台</h1>
            <p>通过自然语言与 AI Agent 交互，完成量子线路构建、模拟执行与结果可视化</p>
        </header>

        <div class="main-row">
            <div class="chat-col">
                <!-- 统计卡片 -->
                <div class="stats-row">
                    <div class="stat-card"><div class="val" id="statSkills">7</div><div class="lbl">技能数</div></div>
                    <div class="stat-card"><div class="val" id="statAlgos">5</div><div class="lbl">量子算法</div></div>
                    <div class="stat-card"><div class="val" id="statAccuracy">94.5%</div><div class="lbl">Grover 精度</div></div>
                    <div class="stat-card"><div class="val" id="statBackends">2</div><div class="lbl">后端数</div></div>
                </div>

                <div id="chatBox" class="chat-box">
                    <div class="msg msg-agent">
                        <div class="msg-label agent-label">🤖 Agent</div>
                        <pre>欢迎使用量子计算 Agent！输入 <b>help</b> 查看可用技能，或点击快捷按钮运行演示。</pre>
                    </div>
                </div>

                <div class="input-row">
                    <input id="inputField" type="text" placeholder="描述您想要的量子计算任务..."
                           onkeydown="if(event.key==='Enter') sendMessage()">
                    <button id="sendBtn" onclick="sendMessage()">发送</button>
                </div>

                <div class="quick-btns">
                    <button onclick="quickCmd('Bell态演示')">⚛ Bell态</button>
                    <button onclick="quickCmd('Grover搜索 目标态 101')">🔍 Grover搜索</button>
                    <button onclick="quickCmd('训练VQC')">🧠 VQC训练</button>
                    <button onclick="quickCmd('平流方程模拟')">🌊 平流方程</button>
                    <button onclick="quickCmd('h(0), cx(0,1)')">🔧 自定义线路</button>
                    <button onclick="quickCmd('help')">❓ 帮助</button>
                </div>
            </div>

            <div class="info-col">
                <div class="skill-panel">
                    <h3>📋 可用技能</h3>
                    <div id="skillList"></div>
                </div>
            </div>
        </div>

        <div class="status-bar">
            Quantum Computing Agent Platform &mdash; 基于 UnitaryLab + Flask
        </div>
    </div>

    <!-- 图片放大弹窗 -->
    <div id="imgModal" class="modal" onclick="this.style.display='none'">
        <img id="modalImg" src="" alt="放大查看">
    </div>

    <script>
        // 自动获取技能列表
        fetch('/api/skills').then(r=>r.json()).then(data=>{
            const list = document.getElementById('skillList');
            list.innerHTML = '';
            (data.skills || []).filter(s => s.id !== 'list_skills').forEach(s => {
                const div = document.createElement('div');
                div.className = 'skill-item';
                div.onclick = () => quickCmd(s.name);
                div.innerHTML = `<div class="name">${s.name}</div><div class="desc">${s.description || ''}</div>`;
                list.appendChild(div);
            });
        });

        function addMessage(label, text, cls='agent-label', status='', vis=null) {
            const box = document.getElementById('chatBox');
            const div = document.createElement('div');
            div.className = 'msg msg-' + (cls === 'user-label' ? 'user' : 'agent');
            let html = `<div class="msg-label ${cls}">${label}`;
            if (status) html += `<span class="msg-status ${status}">${status}</span>`;
            html += `</div><pre>${text}</pre>`;
            if (vis) {
                html += `<div class="msg-vis">`;
                if (vis.endsWith('.svg') || vis.endsWith('.png')) {
                    html += `<img src="/results/plots/${vis.split('/').pop()}" onclick="showModal(this.src)" alt="可视化">`;
                }
                html += `<br><a href="/results/plots/${vis.split('/').pop()}" target="_blank">📊 查看大图</a>`;
                html += `</div>`;
            }
            const t = new Date();
            html += `<div class="msg-time">${t.getHours().toString().padStart(2,'0')}:${t.getMinutes().toString().padStart(2,'0')}:${t.getSeconds().toString().padStart(2,'0')}</div>`;
            div.innerHTML = html;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('inputField');
            const text = input.value.trim();
            if (!text) return;

            addMessage('👤 你', escapeHtml(text), 'user-label');
            input.value = '';
            setLoading(true);

            try {
                const resp = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                });
                const data = await resp.json();
                let output = escapeHtml(data.summary || '无输出');
                if (data.duration_s) {
                    output += `\n⏱ 耗时: ${data.duration_s.toFixed(3)}s`;
                }
                addMessage('🤖 Agent', output, 'agent-label', data.status, data.visualization);
            } catch(e) {
                addMessage('🤖 Agent', '请求失败: ' + e.message, 'agent-label', 'error');
            }
            setLoading(false);
        }

        function quickCmd(text) {
            document.getElementById('inputField').value = text;
            sendMessage();
        }

        function setLoading(v) {
            document.getElementById('sendBtn').className = v ? 'loading' : '';
            document.getElementById('inputField').disabled = v;
        }

        function escapeHtml(s) {
            return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        }

        function showModal(src) {
            document.getElementById('modalImg').src = src;
            document.getElementById('imgModal').style.display = 'flex';
        }
    </script>
</body>
</html>
"""


# ── 路由 ───────────────────────────────────────────────────────────


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"status": "error", "summary": "请输入内容"})

    result = engine.dispatch(text)
    return jsonify({
        "skill": result.skill,
        "status": result.status,
        "summary": result.summary,
        "duration_s": result.duration_s,
        "visualization": result.visualization,
    })


@app.route("/api/skills")
def api_skills():
    skills = engine.list_skills()
    return jsonify({"skills": skills})


@app.route("/api/logs")
def api_logs():
    logs = engine.get_logs()
    return jsonify({"logs": logs})


@app.route("/results/plots/<path:filename>")
def serve_plot(filename):
    """提供结果图片静态文件"""
    return send_from_directory(str(PLOTS_DIR), filename)


# ── 启动 ───────────────────────────────────────────────────────────


def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "").lower() in ("1", "true", "yes")

    print(f"  ⚛  量子计算 Agent Web 平台")
    print(f"  ─────────────────────────────")
    print(f"  URL:  http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print(f"  API:  POST /api/chat   — 自然语言交互")
    print(f"        GET  /api/skills — 列出技能")
    print(f"        GET  /api/logs   — 交互日志")
    print()
    print("  可用技能:")
    for s in engine.list_skills():
        print(f"    ● {s['name']} ({s['id']})")
    print()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()