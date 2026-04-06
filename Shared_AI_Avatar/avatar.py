import streamlit as st
import os
import time
from datetime import datetime

# --- KALI Constants ---
AVATAR_DIR = os.path.dirname(__file__)

def inject_kali_styles():
    """Injects high-end glassmorphism and kinetic CSS for KALI."""
    css_path = os.path.join(AVATAR_DIR, "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline basic styles if file is missing (to prevent complete breakdown)
        st.markdown("""
            <style>
                .avatar-container { background: #000; color: #fff; padding: 20px; border-radius: 10px; }
            </style>
        """, unsafe_allow_html=True)

def render_avatar(state="idle", message="System Ready.", confidence=100, collapsed=False):
    """
    Renders KALI's visual core based on state, message, and confidence.
    Includes a 'collapsed' mode for a minimal HUD.
    """
    inject_kali_styles()
    
    # Init Session States
    if "kali_log_history" not in st.session_state:
        st.session_state.kali_log_history = []
    if "kali_collapsed" not in st.session_state:
        st.session_state.kali_collapsed = collapsed

    # Update Log if message is new
    if message and (not st.session_state.kali_log_history or st.session_state.kali_log_history[-1]['text'] != message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.kali_log_history.append({"time": timestamp, "text": message, "conf": confidence})
        if len(st.session_state.kali_log_history) > 20: st.session_state.kali_log_history.pop(0)

    # 1. THE COLLAPSIBLE TOGGLE (Invisible but fixed position)
    if st.button("🔄 Toggle KALI HUD", key="kali_hud_toggle", use_container_width=True):
        st.session_state.kali_collapsed = not st.session_state.kali_collapsed
        st.rerun()

    # 2. Minimalist HUD Mode (60px Orb)
    if st.session_state.kali_collapsed:
        status_class = f"status-{state}"
        st.markdown(f"""
        <div class="kali-hud-mini {status_class}">
            <div class="neural-orb-mini"></div>
            <div class="mini-tag">KALI_OS :: ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
        return # Exit early for minimal view

    # 3. Full Render (Phase 2 Component structure)
    status_class = f"status-{state}"
    st.markdown(f"""
    <div class="kali-visual-framework {status_class}">
        <div class="orb-platform">
            <div class="orb-aura-glow"></div>
            <div class="neural-orb">
                <div class="orb-core"></div>
                <div class="orb-ring ring-1"></div>
                <div class="orb-ring ring-2"></div>
            </div>
            <div class="status-label-container">
                <span class="pulse-dot"></span>
                <span class="status-text">{state.upper()} MODE</span>
            </div>
        </div>
        <div class="speech-bubble-glass">
            <div class="speech-header"><span class="header-tag">KALI_FEED_V52</span><span class="header-sync">STABLE</span></div>
            <div class="typewriter-body"><p class="typewriter-text">{message}</p></div>
        </div>
        <div class="metrics-panel">
            <div class="metric-header"><span>COGNITIVE CONFIDENCE</span><span>{confidence}%</span></div>
            <div class="meter-track"><div class="meter-fill" style="width: {confidence}%;"></div></div>
        </div>
        <div class="hud-labels">
            <span class="kbd-hint">Press K to focus KALI input</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. KALI History Log (Persistent Expander)
    with st.expander("📝 KALI SENSORY BACKLOG", expanded=False):
        for entry in reversed(st.session_state.kali_log_history):
            st.markdown(f"**[{entry['time']}]** {entry['text']} *(Confidence: {entry['conf']}% )*")

def explain_chart(chart_title, data_summary):
    """Triggered by 'Ask KALI' button under charts."""
    from kali_brain import ask_kali
    st.session_state.kali_status = "thinking"
    msg = "".join(list(ask_kali(f"Explain this {chart_title} chart in 2 precise witty sentences: {data_summary}")))
    st.session_state.kali_message = msg
    st.rerun()

# Exporting for Mission_Control
__all__ = ['render_avatar', 'explain_chart']
