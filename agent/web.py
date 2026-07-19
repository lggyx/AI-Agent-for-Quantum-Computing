"""
Quantum Agent Web — Flask 轻量版 Web 演示平台

提供 Web 界面和 REST API 两种交互方式。
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string, request

from agent.skills import get_engine

app = Flask(__name__)
engine = get_engine()

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
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        header {
            text-align: center; padding: 30px 0 20px;
            border-bottom: 1px solid #1e2a45;
        }
        header h1 {
            font-size: 1.8rem; background: linear-gradient(135deg, #6c8cff, #00d4aa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        header p { color: #8892b0; margin-top: 8px; font-size: 0.9rem; }
        .chat-box {
            margin: 20px 0; background: #111827; border-radius: 12px;
            border: 1px solid #1e2a45; min-height: 400px; max-height: 500px;
            overflow-y: auto; padding: 16px;
        }
        .msg { margin-bottom: 12px; }
        .msg-user {
            background: #1a2340; border-radius: 8px 8px 8px 0;
            padding: 10px 14px; max-width: 80%; margin-left: auto;
            border: 1px solid #2a3a5a;
        }
        .msg-agent {
            background: #0f1a2e; border-radius: 8px 8px 0 8px;
            padding: 10px 14px; max-width: 90%; margin-right: auto;
            border: 1px solid #1a2a44;
        }
        .msg-agent pre {
            white-space: pre-wrap; font-family: inherit; font-size: 0.85rem;
            line-height: 1.6; color: #c8d0e0;
        }
        .msg-label { font-size: 0.75rem; color: #6c8cff; margin-bottom: 4px; font-weight: bold; }
        .msg-label.user-label { color: #00d4aa; text-align: right; }
        .msg-label.agent-label { color: #6c8cff; }
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
        /* status colors */
        .ok { color: #00d4aa; }
        .error { color: #ff5a5a; }
        .env_unavailable { color: #ffaa33; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚛ 量子计算 Agent 演示平台</h1>
            <p>通过自然语言与 AI Agent 交互，完成量子线路构建、模拟执行与结果可视化</p>
        </header>

        <div id="chatBox" class="chat-box">
            <div class="msg msg-agent">
                <div class="msg-label agent-label">🤖 Agent</div>
                <pre>欢迎使用量子计算 Agent！输入 <b>help</b> 查看可用技能。</pre>
            </div>
        </div>

        <div class="input-row">
            <input id="inputField" type="text" placeholder="描述您想要的量子计算任务..."
                   onkeydown="if(event.key==='Enter') sendMessage()">
            <button id="sendBtn" onclick="sendMessage()">发送</button>
        </div>

        <div class="quick-btns">
            <button onclick="quickCmd('Bell态演示')">Bell态演示</button>
            <button onclick="quickCmd('Grover搜索 目标态 101')">Grover搜索</button>
            <button onclick="quickCmd('训练VQC 1层 2个epoch')">VQC训练</button>
            <button onclick="quickCmd('平流方程模拟')">平流方程</button>
            <button onclick="quickCmd('h(0), cx(0,1)')">自定义线路</button>
            <button onclick="quickCmd('help')">帮助</button>
        </div>

        <div class="status-bar">
            Quantum Computing Agent Platform &mdash; 基于 UnitaryLab + Flask
        </div>
    </div>

    <script>
        function addMessage(label, text, cls='agent-label') {
            const box = document.getElementById('chatBox');
            const div = document.createElement('div');
            div.className = 'msg msg-' + (cls === 'user-label' ? 'user' : 'agent');
            div.innerHTML = `<div class="msg-label ${cls}">${label}</div><pre>${text}</pre>`;
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
                if (data.visualization) {
                    output += `\n\n📊 可视化: ${data.visualization}`;
                }
                addMessage('🤖 Agent (' + data.status + ')', output, 'agent-label');
            } catch(e) {
                addMessage('🤖 Agent (error)', '请求失败: ' + e.message, 'agent-label');
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
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()