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
:root{--bg:#0d0f14;--surface:#141720;--border:#1e2330;--accent:#5b7fff;--accent2:#a78bfa;--green:#34d399;--text:#e8eaf0;--muted:#6b7280;--radius:14px}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--bg)!important;color:var(--text)!important}
#MainMenu,footer,header{visibility:hidden}.stDeployButton{display:none}[data-testid="stToolbar"]{display:none}
.main .block-container{max-width:820px;padding:2rem 1.5rem 4rem;margin:0 auto}
.ts-header{text-align:center;padding:2.5rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem}
.ts-logo{font-family:'Syne',sans-serif;font-weight:800;font-size:2rem;letter-spacing:-0.03em;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.ts-tagline{color:var(--muted);font-size:.88rem;font-weight:300;letter-spacing:.08em;text-transform:uppercase;margin-top:.3rem}
.ts-status{display:flex;align-items:center;gap:.5rem;background:var(--surface);border:1px solid var(--border);border-radius:50px;padding:.4rem 1rem;font-size:.78rem;color:var(--muted);width:fit-content;margin:0 auto 1.8rem}
.ts-dot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.chat-wrap{display:flex;flex-direction:column;gap:1rem;margin-bottom:1.5rem}
.msg{display:flex;gap:.75rem;animation:fadein .3s ease}
@keyframes fadein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg-user{flex-direction:row-reverse}
.msg-avatar{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.95rem;flex-shrink:0}
.avatar-bot{background:linear-gradient(135deg,var(--accent),var(--accent2))}
.avatar-user{background:var(--surface);border:1px solid var(--border)}
.msg-bubble{max-width:78%;padding:.85rem 1.1rem;border-radius:var(--radius);font-size:.91rem;line-height:1.65}
.bubble-bot{background:var(--surface);border:1px solid var(--border);border-bottom-left-radius:4px;color:var(--text)}
.bubble-user{background:linear-gradient(135deg,rgba(91,127,255,.13),rgba(167,139,250,.13));border:1px solid rgba(91,127,255,.27);border-bottom-right-radius:4px;color:var(--text)}
.progress-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.25rem;margin-bottom:1.5rem}
.progress-title{font-family:'Syne',sans-serif;font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:.6rem}
.progress-steps{display:flex;gap:.4rem;flex-wrap:wrap}
.step-pill{padding:.2rem .65rem;border-radius:50px;font-size:.75rem;font-weight:500}
.step-done{background:rgba(52,211,153,.13);color:var(--green);border:1px solid rgba(52,211,153,.27)}
.step-active{background:rgba(91,127,255,.13);color:var(--accent);border:1px solid rgba(91,127,255,.27)}
.step-todo{background:transparent;color:var(--muted);border:1px solid var(--border)}
.stTextInput>div>div>input{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;font-size:.92rem!important;padding:.75rem 1rem!important}
.stTextInput>div>div>input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(91,127,255,.12)!important}
.stTextInput>div>div>input::placeholder{color:var(--muted)!important}
.stButton>button{background:linear-gradient(135deg,var(--accent),var(--accent2))!important;color:white!important;border:none!important;border-radius:var(--radius)!important;font-family:'Syne',sans-serif!important;font-weight:600!important;font-size:.88rem!important;padding:.6rem 1.6rem!important}
.stButton>button:hover{opacity:.88!important}
.ts-info{background:rgba(91,127,255,.05);border:1px solid rgba(91,127,255,.2);border-radius:var(--radius);padding:.75rem 1rem;font-size:.83rem;color:var(--muted);margin-bottom:1rem}
hr{border-color:var(--border)!important;margin:1.5rem 0!important}
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
  <div class="ts-tagline">AI-Powered Hiring Assistant · Technology Placements</div>
</div>
<div class="ts-status"><div class="ts-dot"></div>Online · Powered by Groq LLaMA-3</div>
""", unsafe_allow_html=True)

# ── Progress bar ──────────────────────────────────────────────────────────────
STAGES = ["greeting","info_gathering","tech_stack","tech_questions","farewell"]
LABELS = {"greeting":"👋 Welcome","info_gathering":"📋 Profile","tech_stack":"🛠 Tech Stack","tech_questions":"🧠 Assessment","farewell":"✅ Complete"}

def render_progress():
    cur = st.session_state.stage
    pills = ""
    for s in STAGES:
        ci, si = STAGES.index(cur), STAGES.index(s)
        cls = "step-done" if si < ci else ("step-active" if si == ci else "step-todo")
        pills += f'<span class="step-pill {cls}">{LABELS[s]}</span>'
    st.markdown(f'<div class="progress-card"><div class="progress-title">Interview Progress</div><div class="progress-steps">{pills}</div></div>', unsafe_allow_html=True)

render_progress()

# ── Messages ──────────────────────────────────────────────────────────────────
def render_messages():
    html = '<div class="chat-wrap">'
    for m in st.session_state.messages:
        c = m["content"].replace("\n","<br>")
        if m["role"] == "assistant":
            html += f'<div class="msg"><div class="msg-avatar avatar-bot">🎯</div><div class="msg-bubble bubble-bot">{c}</div></div>'
        else:
            html += f'<div class="msg msg-user"><div class="msg-avatar avatar-user">👤</div><div class="msg-bubble bubble-user">{c}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

if not st.session_state.messages:
    st.session_state.messages.append({"role":"assistant","content":st.session_state.chat_engine.get_greeting()})

render_messages()

# ── Input ─────────────────────────────────────────────────────────────────────
EXIT_KW = {"exit","quit","bye","goodbye","stop","end"}

if not st.session_state.session_ended:
    st.markdown('<div class="ts-info">💡 Type your response below. Say <strong>exit</strong>, <strong>quit</strong>, or <strong>bye</strong> to end the session.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([5,1])
    with c1:
        user_input = st.text_input("msg", key=f"inp_{st.session_state.input_key}", placeholder="Type your response here…", label_visibility="collapsed")
    with c2:
        send = st.button("Send →", use_container_width=True)

    if (send or user_input) and user_input.strip():
        text = user_input.strip()
        st.session_state.messages.append({"role":"user","content":text})

        if any(kw in text.lower() for kw in EXIT_KW):
            farewell = st.session_state.chat_engine.get_farewell(st.session_state.candidate)
            st.session_state.messages.append({"role":"assistant","content":farewell})
            st.session_state.stage = "farewell"
            st.session_state.session_ended = True
            st.session_state.data_handler.save_candidate(st.session_state.candidate, st.session_state.messages)
        else:
            resp, new_stage, updated = st.session_state.chat_engine.process_turn(
                text, st.session_state.stage, st.session_state.candidate, st.session_state.messages[:-1]
            )
            st.session_state.messages.append({"role":"assistant","content":resp})
            st.session_state.stage = new_stage
            st.session_state.candidate = updated
            if new_stage == "farewell":
                st.session_state.session_ended = True
                st.session_state.data_handler.save_candidate(st.session_state.candidate, st.session_state.messages)

        st.session_state.input_key += 1
        st.rerun()
else:
    st.markdown('<div style="text-align:center;padding:2rem;color:#6b7280"><div style="font-size:2rem;margin-bottom:.5rem">✅</div><strong style="color:#e8eaf0">Session Complete</strong><br><span style="font-size:.85rem">Thank you for your time. We\'ll be in touch shortly!</span></div>', unsafe_allow_html=True)
    if st.button("🔄 Start New Session"):
        for k in ["messages","stage","candidate","session_ended","input_key"]:
            del st.session_state[k]
        st.session_state.chat_engine = ChatEngine()
        st.rerun()
