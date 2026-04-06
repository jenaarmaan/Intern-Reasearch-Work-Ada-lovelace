import streamlit as st
import time
import base64
import textwrap
from datetime import datetime
from kali_brain import ask_kali

# --- KALI UI Engine ---
def render_safe(html_content: str):
    """Sanitizes and safely renders KALI OS visual components by removing markdown fences."""
    if not html_content: return
    # CRITICAL: Strip all surrounding whitespace/tabs and dedicatedly dedent
    clean_html = textwrap.dedent(html_content).strip()
    # If the string STILL starts with a code block indicator or spaces, strip them manually
    while clean_html.startswith(("`", "\n", " ")):
        clean_html = clean_html.lstrip("`").lstrip("\n").lstrip(" ")
    
    processed_html = clean_html.replace("<hr>", "<div class='kali-divider-line'></div>")
    st.markdown(processed_html, unsafe_allow_html=True)

def render_avatar(state="idle", message="", confidence=100.0, collapsed=False):
    """
    Renders KALI's physical presence and HUD.
    """
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    status_class = f"status-{state}"
    ring_speed = "slow" if state == "idle" else "fast" if state == "thinking" else "static"
    pulse_color = "#00f2ff" if state == "idle" else "#bc13fe" if state == "thinking" else "#ff3c3c"
    
    if collapsed:
        render_safe(f"""
        <div class="kali-hud-mini {status_class}">
            <div class="neural-orb-mini"></div>
            <div class="mini-tag">KALI ONLINE</div>
        </div>
        """)
        return

    # FULL HUD 
    render_safe(f"""
    <div class="kali-visual-framework {status_class}">
        <div class="orb-platform-pro">
            <div class="orb-aura-glow-v2"></div>
            <div class="neural-orb-pro">
                <div class="orb-core-v2"></div>
                <div class="orb-outer-ring {ring_speed}-spin"></div>
            </div>
            <div class="status-pill-v2">
                <span class="pulse-dot-v2" style="background: {pulse_color}; box-shadow: 0 0 10px {pulse_color};"></span>
                <span class="status-text-v2">{state.upper()} MODE</span>
            </div>
        </div>
        
        <div class="speech-bubble-pro">
            <div class="speech-header-pro">
                <span class="header-node">KALI_OS_NEXUS</span>
                <span class="header-timestamp">{datetime.now().strftime('%H:%M:%S')}</span>
            </div>
            <div class="typewriter-container">
                <p class="kali-dialogue">{message}<span class="typing-cursor">|</span></p>
            </div>
        </div>
        
        <div class="metrics-hub">
            <div class="metric-info">
                <span class="metric-tag">COGNITIVE CONFIDENCE</span>
                <span class="metric-val">{confidence}%</span>
            </div>
            <div class="meter-system">
                <div class="meter-track-v2">
                    <div class="meter-fill-v2" style="width: {confidence}%;"></div>
                    <div class="meter-ticks">
                        <span class="tick" style="left:25%"></span>
                        <span class="tick" style="left:50%"></span>
                        <span class="tick" style="left:75%"></span>
                        <span class="tick" style="left:100%"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)

    with st.expander("📂 KALI SENSORY BACKLOG", expanded=False):
        if not st.session_state.get("kali_history"):
            st.caption("Sensory buffers cleared. Waiting for interaction...")
        else:
            for entry in reversed(st.session_state.kali_history):
                timestamp = entry.get("timestamp", "00:00:00")
                role = "USER" if entry["role"] == "user" else "KALI"
                text = entry["content"]
                conf = entry.get("confidence", "100")
                
                st.markdown(f"""
                <div class="backlog-row">
                    <div class="backlog-header">
                        <span class="backlog-time">[{timestamp}]</span>
                        <span class="backlog-role">{role} :: {conf}%</span>
                    </div>
                    <div class="backlog-text">{text}</div>
                </div>
                """, unsafe_allow_html=True)

def render_system_status():
    """Renders the comprehensive KALI System Status panel for the right column."""
    duration = int(time.time() - st.session_state.get("start_time", time.time()))
    latency = st.session_state.get("kali_latency", "0.8s")
    
    render_safe(f"""
    <div class="system-status-pnl">
        <h3 class="pnl-title">KALI SYSTEM STATUS</h3>
        <div class="status-grid">
            <div class="status-item"><span class="lbl">AURA STATE</span><span class="val">{st.session_state.get('kali_status', 'IDLE')}</span></div>
            <div class="status-item"><span class="lbl">SESSION UPTIME</span><span class="val">{duration}s</span></div>
            <div class="status-item"><span class="lbl">LOGS GENERATED</span><span class="val">{len(st.session_state.get('kali_history', []))}</span></div>
            <div class="status-item"><span class="lbl">BRAIN LATENCY</span><span class="val">{latency}</span></div>
            <div class="status-item"><span class="lbl">NEXUS TIME</span><span class="val clock">{datetime.now().strftime('%H:%M:%S')}</span></div>
        </div>
    </div>
    """)

def explain_chart(chart_title, data_summary):
    """Triggered by 'Ask KALI' button under charts."""
    prompt = f"Analyze this chart result for '{chart_title}'. Summary data: {data_summary}. Explain in 2 sentences."
    st.session_state.kali_status = "thinking"
    st.session_state.kali_message = ""
    for token in ask_kali(prompt, context="Chart Analysis"):
        st.session_state.kali_message += token
    st.session_state.kali_status = "speaking"
    st.rerun()
