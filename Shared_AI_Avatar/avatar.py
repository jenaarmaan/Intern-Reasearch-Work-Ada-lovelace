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
    Renders KALI's physical presence using simple, clean components.
    """
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    # Simple Avatar Circle with Pulse
    st.markdown(f'''
        <div class="kali-card" style="text-align: center;">
            <div class="avatar-pulse">K</div>
            <div style="margin-top: 15px; font-weight: 600; color: #4A90D9;">
                KALI — {state.upper()}
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Clean Message Display
    if message:
        if state == "thinking":
            st.info(message)
        elif state == "error":
            st.error(message)
        else:
            st.success(message)

    # Confidence Meter
    st.progress(confidence / 100.0, text=f"Cognitive Confidence: {confidence}%")

    with st.expander("📂 Interaction History", expanded=False):
        if not st.session_state.get("kali_history"):
            st.caption("No recent interactions.")
        else:
            for entry in reversed(st.session_state.kali_history):
                role = "USER" if entry["role"] == "user" else "KALI"
                st.write(f"**{role}:** {entry['content']}")

def render_system_status():
    """Renders a simple system status panel."""
    duration = int(time.time() - st.session_state.get("start_time", time.time()))
    
    st.markdown('<div class="kali-card">', unsafe_allow_html=True)
    st.subheader("System Status")
    st.write(f"**State:** {st.session_state.get('kali_status', 'IDLE').upper()}")
    st.write(f"**Uptime:** {duration}s")
    st.write(f"**Latency:** {st.session_state.get('kali_latency', '0.8s')}")
    st.write(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)

def explain_chart(chart_title, data_summary):
    """Triggered by 'Ask KALI' button under charts."""
    prompt = f"Analyze this chart result for '{chart_title}'. Summary data: {data_summary}. Explain in 2 sentences."
    st.session_state.kali_status = "thinking"
    st.session_state.kali_message = ""
    for token in ask_kali(prompt, context="Chart Analysis"):
        st.session_state.kali_message += token
    st.session_state.kali_status = "idle" 
    st.rerun()
