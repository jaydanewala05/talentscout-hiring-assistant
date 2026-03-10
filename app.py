"""
TalentScout - AI Hiring Assistant
Main Streamlit Application
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from utils.chat_engine import ChatEngine
from utils.data_handler import DataHandler

st.set_page_config(
    page_title="TalentScout | AI Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:      #0a0c10;
    --surface: #111318;
    --surface2:#161a24;
    --border:  #1f2433;
    --accent:  #5b7fff;
    --accent2: #a78bfa;
    --green:   #34d399;
    --red:     #f87171;
    --text:    #dde1ec;
    --muted:   #555f7a;
    --radius:  16px;
}

/* ── Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── Layout ── */
.main .block-container {
    max-width: 780px;
    padding: 1.5rem 1.5rem 5rem;
    margin: 0 auto;
}

/* ── Header ── */
.ts-header {
    text-align: center;
    padding: 2rem 0 1.2rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.ts-header::after {
    content: '';
    display: block;
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    margin: 1rem auto 0;
    border-radius: 2px;
}
.ts-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.9rem;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, var(--accent) 30%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.ts-tagline {
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── Status pill ── */
.ts-status {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 50px;
    padding: 0.35rem 0.9rem;
    font-size: 0.73rem;
    color: var(--muted);
    width: fit-content;
    margin: 0 auto 1.6rem;
    letter-spacing: 0.03em;
}
.ts-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green);
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* ── Progress ── */
.progress-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.85rem 1.1rem;
    margin-bottom: 1.4rem;
}
.progress-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: var(--muted);
    margin-bottom: 0.55rem;
}
.progress-steps { display: flex; gap: 0.35rem; flex-wrap: wrap; }
.step-pill {
    padding: 0.18rem 0.6rem;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.01em;
}
.step-done   { background: rgba(52,211,153,.12); color:#34d399; border:1px solid rgba(52,211,153,.22); }
.step-active { background: rgba(91,127,255,.15); color:#7c9fff; border:1px solid rgba(91,127,255,.3); }
.step-todo   { background: transparent;          color:var(--muted); border:1px solid var(--border); }

/* ── Chat ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    margin-bottom: 1.2rem;
}
.msg {
    display: flex;
    gap: 0.65rem;
    animation: fadein 0.25s ease;
}
@keyframes fadein { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
.msg-user { flex-direction: row-reverse; }

.msg-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar-bot  { background: linear-gradient(135deg,var(--accent),var(--accent2)); }
.avatar-user { background: #1e2235; border: 1px solid #2a2f45; color: #7c9fff; font-size:0.8rem; font-weight:600; }

/* BOT bubble */
.bubble-bot {
    max-width: 75%;
    padding: 0.8rem 1rem;
    border-radius: 0 var(--radius) var(--radius) var(--radius);
    font-size: 0.89rem;
    line-height: 1.7;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
}

/* USER bubble — dark with subtle blue tint */
.bubble-user {
    max-width: 65%;
    padding: 0.7rem 1rem;
    border-radius: var(--radius) 0 var(--radius) var(--radius);
    font-size: 0.89rem;
    line-height: 1.65;
    background: #1a1f35;
    border: 1px solid #252d4a;
    color: #c8d0f0;
}

/* ── Hint bar ── */
.ts-info {
    background: rgba(91,127,255,.04);
    border: 1px solid rgba(91,127,255,.14);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 0.7rem;
    letter-spacing: 0.01em;
}
.ts-info strong { color: #7c9fff; }

/* ── Input ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #3d5acc !important;
    box-shadow: 0 0 0 3px rgba(61,90,204,.1) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── Send button ── */
.stButton > button {
    background: linear-gradient(135deg, #4a6ef5, #7c5ce4) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.6rem 1.2rem !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

/* ── Complete screen ── */
.ts-complete {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--muted);
}
.ts-complete .icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.ts-complete strong { color: var(--text); font-size: 1.05rem; }
.ts-complete p { font-size: 0.85rem; margin-top: 0.4rem; color: var(--muted); }

hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session init ──────────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "messages":      [],
        "stage":         "greeting",
        "candidate":     {},
        "chat_engine":   ChatEngine(),
        "data_handler":  DataHandler(),
        "session_ended": False,
        "input_key":     0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ts-header">
  <div class="ts-logo">🎯 TalentScout</div>
  <div class="ts-tagline">AI-Powered Hiring Assistant &nbsp;·&nbsp; Technology Placements</div>
</div>
<div class="ts-status">
  <div class="ts-dot"></div>
  Online &nbsp;·&nbsp; Powered by Groq LLaMA-3
</div>
""", unsafe_allow_html=True)

# ── Progress ──────────────────────────────────────────────────────────────────
STAGES = ["greeting","info_gathering","tech_stack","tech_questions","farewell"]
LABELS = {
    "greeting":       "👋 Welcome",
    "info_gathering": "📋 Profile",
    "tech_stack":     "🛠 Tech Stack",
    "tech_questions": "🧠 Assessment",
    "farewell":       "✅ Complete",
}

def render_progress():
    cur = st.session_state.stage
    pills = ""
    for s in STAGES:
        ci, si = STAGES.index(cur), STAGES.index(s)
        cls = "step-done" if si < ci else ("step-active" if si == ci else "step-todo")
        pills += f'<span class="step-pill {cls}">{LABELS[s]}</span>'
    st.markdown(
        f'<div class="progress-card">'
        f'<div class="progress-title">Interview Progress</div>'
        f'<div class="progress-steps">{pills}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

render_progress()

# ── Messages ──────────────────────────────────────────────────────────────────
def render_messages():
    html = '<div class="chat-wrap">'
    for m in st.session_state.messages:
        c = m["content"].replace("\n", "<br>")
        if m["role"] == "assistant":
            html += (
                f'<div class="msg">'
                f'<div class="msg-avatar avatar-bot">🎯</div>'
                f'<div class="bubble-bot">{c}</div>'
                f'</div>'
            )
        else:
            html += (
                f'<div class="msg msg-user">'
                f'<div class="msg-avatar avatar-user">YOU</div>'
                f'<div class="bubble-user">{c}</div>'
                f'</div>'
            )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

if not st.session_state.messages:
    greeting = st.session_state.chat_engine.get_greeting()
    st.session_state.messages.append({"role": "assistant", "content": greeting})

render_messages()

# ── Input ─────────────────────────────────────────────────────────────────────
EXIT_KW = {"exit", "quit", "bye", "goodbye", "stop", "end"}

if not st.session_state.session_ended:
    st.markdown(
        '<div class="ts-info">'
        '💡 Type your response below. Say <strong>exit</strong>, <strong>quit</strong>, or <strong>bye</strong> to end the session.'
        '</div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([5, 1])
    with c1:
        user_input = st.text_input(
            "msg",
            key=f"inp_{st.session_state.input_key}",
            placeholder="Type your response here…",
            label_visibility="collapsed",
        )
    with c2:
        send = st.button("Send →", use_container_width=True)

    if (send or user_input) and user_input.strip():
        text = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": text})

        if any(kw in text.lower() for kw in EXIT_KW):
            farewell = st.session_state.chat_engine.get_farewell(st.session_state.candidate)
            st.session_state.messages.append({"role": "assistant", "content": farewell})
            st.session_state.stage = "farewell"
            st.session_state.session_ended = True
            st.session_state.data_handler.save_candidate(
                st.session_state.candidate, st.session_state.messages
            )
        else:
            resp, new_stage, updated = st.session_state.chat_engine.process_turn(
                text,
                st.session_state.stage,
                st.session_state.candidate,
                st.session_state.messages[:-1],
            )
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.session_state.stage = new_stage
            st.session_state.candidate = updated
            if new_stage == "farewell":
                st.session_state.session_ended = True
                st.session_state.data_handler.save_candidate(
                    st.session_state.candidate, st.session_state.messages
                )

        st.session_state.input_key += 1
        st.rerun()

else:
    st.markdown("""
    <div class="ts-complete">
        <div class="icon">✅</div>
        <strong>Session Complete</strong>
        <p>Thank you for your time. Our team will review your profile and reach out within 2–3 business days.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Start New Session"):
        for k in ["messages", "stage", "candidate", "session_ended", "input_key"]:
            del st.session_state[k]
        st.session_state.chat_engine = ChatEngine()
        st.rerun()