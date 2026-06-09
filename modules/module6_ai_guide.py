import streamlit as st
import requests
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data.region_data import REGION_DB, SPECIES_DB, STATUS_LABEL

# ── 系统提示词 ─────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """你是"生物多样性探索"应用的专业 AI 讲解员。你的名字叫"绿野"。

你的专业背景：
- 生态学、保育生物学和科学教育
- 熟悉 IUCN 濒危物种红色名录
- 了解全球各大生态系统和生物多样性热点地区
- 擅长用通俗易懂的方式向普通大众讲解科学知识

你的讲解风格：
- 语气友好、热情，像一位热爱自然的向导
- 用生动的比喻和故事让知识更有趣
- 回答准确，但避免过于专业的术语
- 适时引入危机感，激发保护意识
- 每次回答控制在 300 字以内，除非用户要求详细

你可以帮助用户：
1. 了解某个地区的生物多样性状况
2. 介绍特定物种的习性、现状和保护故事
3. 解释 IUCN 濒危等级和保护意义
4. 分析某地区面临的环境威胁
5. 推荐值得关注的濒危物种
6. 解答生态学基础概念（食物链、生态系统、特有物种等）

回答时请：
- 在适当位置加入 emoji 让内容更活泼 🌿🦁🐠
- 如果涉及数字，尽量给出直观的类比
- 结尾可以留一个小问题引导用户继续探索

如果用户询问的内容超出生物多样性范围，友善地引导回主题。
"""

QUICK_QUESTIONS = [
    "🌍 哪个地区的生物多样性最丰富？",
    "🦁 什么是 IUCN 极危物种？",
    "🐼 大熊猫为什么濒危？",
    "🐝 蜜蜂消失对生态系统有什么影响？",
    "🌊 珊瑚礁为什么被称为海洋热带雨林？",
    "🦋 帝王蝶的迁徙有多神奇？",
    "🐧 气候变化如何威胁极地物种？",
    "🌿 什么是特有物种？为什么重要？",
    "🔴 物种灭绝有哪些连锁反应？",
    "🦏 犀牛角为什么引来偷猎危机？",
]

def _call_api(messages: list, api_key: str, base_url: str, model: str) -> str:
    """通用 API 调用（支持 OpenAI 兼容接口）"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "temperature": 0.75,
        "max_tokens": 800,
        "stream": False,
    }
    try:
        resp = requests.post(
            f"{base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "⏳ 请求超时，请检查网络后重试。"
    except requests.exceptions.ConnectionError:
        return "🌐 连接失败，请检查 Base URL 是否正确。"
    except Exception as e:
        err = str(e)
        if "401" in err or "authentication" in err.lower():
            return "🔑 API 认证失败，请在侧边栏检查 API Key。"
        elif "429" in err or "rate_limit" in err.lower():
            return "⏳ 请求频率过高，请稍后再试。"
        return f"❌ 请求失败：{err[:200]}"


def _build_region_context(region_name: str) -> str:
    """把当前地区数据注入上下文，让 AI 回答更精准"""
    if region_name not in REGION_DB:
        return ""
    d = REGION_DB[region_name]
    species_names = "、".join([s["name"] for s in d["species"]])
    threats_text = "、".join([t[0] for t in d["threats"][:3]])
    return (
        f"\n[当前用户正在查看：{region_name}]\n"
        f"生态系统：{d['biome']}\n"
        f"已知物种：{d['total_species']}，濒危物种：{d['endangered']} 种\n"
        f"特有物种率：{d['endemic_pct']}%，多样性指数：{d['score']}\n"
        f"代表物种：{species_names}\n"
        f"主要威胁：{threats_text}\n"
    )


def render_ai_guide():
    st.title("🤖 AI 生物多样性讲解员")
    st.caption("你好！我是绿野，你的专属生物多样性导游 🌿 有任何问题都可以问我！")

    # ── API 配置（侧边栏内嵌） ──────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🤖 AI 讲解员设置")
        api_key = st.text_input(
            "API Key",
            type="password",
            key="ai_guide_api_key",
            placeholder="sk-... 或 your-key",
            help="支持 DeepSeek / OpenAI / 任何兼容 OpenAI 格式的 API",
        )
        base_url = st.text_input(
            "Base URL",
            value="https://api.deepseek.com",
            key="ai_guide_base_url",
            help="DeepSeek: https://api.deepseek.com | OpenAI: https://api.openai.com",
        )
        model = st.text_input(
            "模型名称",
            value="deepseek-chat",
            key="ai_guide_model",
            help="deepseek-chat / gpt-4o-mini / gpt-3.5-turbo 等",
        )

        # 上下文注入：选择当前地区
        st.markdown("---")
        st.markdown("**📍 注入地区上下文（可选）**")
        context_region = st.selectbox(
            "让 AI 了解你正在看哪个地区",
            ["无"] + list(REGION_DB.keys()),
            key="ai_context_region",
        )

        if st.button("🗑️ 清空对话", use_container_width=True, key="clear_ai_chat"):
            st.session_state["ai_guide_messages"] = []
            st.rerun()

    # ── Session State ──────────────────────────────────
    if "ai_guide_messages" not in st.session_state:
        st.session_state["ai_guide_messages"] = []

    # ── 快速提问按钮 ────────────────────────────────────
    if not st.session_state["ai_guide_messages"]:
        st.markdown("**💡 快速提问（点击即发送）**")
        cols = st.columns(2)
        for i, q in enumerate(QUICK_QUESTIONS):
            with cols[i % 2]:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    st.session_state["ai_guide_messages"].append(
                        {"role": "user", "content": q}
                    )
                    st.session_state["ai_pending"] = True
                    st.rerun()
        st.markdown("---")

    # ── 渲染历史消息 ────────────────────────────────────
    for msg in st.session_state["ai_guide_messages"]:
        with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "🧑"):
            st.markdown(msg["content"])

    # ── 处理待发送消息（快速提问触发）──────────────────
    if st.session_state.get("ai_pending"):
        st.session_state["ai_pending"] = False
        _process_ai_response(api_key, base_url, model, context_region)
        st.rerun()

    # ── 用户输入 ────────────────────────────────────────
    user_input = st.chat_input("问我任何关于生物多样性的问题...")
    if user_input:
        st.session_state["ai_guide_messages"].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)
        _process_ai_response(api_key, base_url, model, context_region)

    # ── 未配置 API 时的提示 ────────────────────────────
    if not api_key and not st.session_state["ai_guide_messages"]:
        st.info("👈 请在左侧侧边栏填写 API Key 后开始对话。支持 DeepSeek、OpenAI 等兼容接口。")


def _process_ai_response(api_key, base_url, model, context_region):
    """调用 AI 并追加回复"""
    if not api_key:
        reply = "🔑 请先在侧边栏填写 API Key 才能开始对话！"
        st.session_state["ai_guide_messages"].append(
            {"role": "assistant", "content": reply}
        )
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(reply)
        return

    # 构建带上下文的消息列表
    messages = []
    if context_region and context_region != "无":
        ctx = _build_region_context(context_region)
        if ctx:
            messages.append({"role": "system", "content": ctx})

    # 加入对话历史（最近 10 轮）
    history = st.session_state["ai_guide_messages"]
    for m in history[-20:]:
        if m["role"] in ("user", "assistant"):
            messages.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("绿野正在思考中...🌿"):
            reply = _call_api(messages, api_key, base_url, model)
        st.markdown(reply)

    st.session_state["ai_guide_messages"].append(
        {"role": "assistant", "content": reply}
    )
