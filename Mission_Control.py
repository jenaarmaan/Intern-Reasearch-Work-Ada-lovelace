import streamlit as st
import sys
import os
import time
from datetime import datetime

# --- Path Integration Hub (MUST BE AT TOP) ---
def add_path(folder):
    """Integrates secondary research modules into the runtime path."""
    p = os.path.abspath(folder)
    if p not in sys.path: sys.path.append(p)

# Root level folders
add_path("Shared_Core")
add_path("Shared_AI_Avatar")
add_path("Assignment_1")
add_path("Assignment_2")

# Now import the modules
try:
    from avatar import render_avatar, explain_chart, render_system_status
    from theory_docs import run_theoretical_info, run_project_docs
    from avatar_specs import run_avatar_specs
    # These three are currently causing the ImportError
    from kali_proactive import check_proactive_triggers, safe_run, run_kali_walkthrough
    from kali_brain import ask_kali, get_confidence
    from kali_voice import listen, speak
except ImportError as e:
    st.error(f"KALI System Node Sync Failure: {e}")
    st.stop()

import Assignment_1.app_module as a1
import Assignment_2.app_module as a2

# --- KALI Session Initialization ---
def init_kali_session():
    """Ensures KALI's cognitive states are initialized in the correct order."""
    if "kali_status" not in st.session_state: st.session_state.kali_status = "idle"
    if "kali_message" not in st.session_state: st.session_state.kali_message = "KALI Core Ready. Portals Synchronized."
    if "kali_query" not in st.session_state: st.session_state.kali_query = None
    if "kali_muted" not in st.session_state: st.session_state.kali_muted = False
    if "last_interaction" not in st.session_state: st.session_state.last_interaction = time.time()
    if "kali_history" not in st.session_state: st.session_state.kali_history = []
    if "kali_best_sharpe" not in st.session_state: st.session_state.kali_best_sharpe = 0.0
    if "kali_ready" not in st.session_state: st.session_state.kali_ready = False

init_kali_session()

# --- Page Config ---
st.set_page_config(
    page_title="KALI — Quantum Learning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS LOAD ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("Shared_AI_Avatar/style.css")

# Navigation
with st.sidebar:
    st.title("KALI")
    st.caption("Quantum Learning Assistant")
    
    st.sidebar.header("Navigation")
    nav_options = {
        "PORTFOLIO OPTIMIZER (A2)": "teal",
        "TECHNICAL REPORT (A1)": "gray",
        "KALI AVATAR CORE": "red",
        "THEORETICAL CONCEPTS": "gray",
        "PROJECT DOCUMENTATION": "gray"
    }
    nav = st.radio("Select Page", list(nav_options.keys()), label_visibility="collapsed")
    
    st.sidebar.header("Controls")
    if st.button("🚀 Sync Walkthrough", use_container_width=True):
        run_kali_walkthrough()
    
    st.sidebar.header("AI Glossary")
    with st.expander("Terms"):
        st.button("Sharpe Ratio", help="KALI: The mathematical reward-to-variability ratio.", use_container_width=True)
        st.button("Ry-Gate", help="KALI: My primary quantum rotation actuator.", use_container_width=True)
    
    st.markdown("---")
    status_type = "nominal" if st.session_state.kali_status == "idle" else "alert"
    st.markdown(f"<div class='status-capsule status-{status_type}'>STATUS: {st.session_state.kali_status.upper()}</div>", unsafe_allow_html=True)

# Main Header
st.title("KALI — Quantum Learning Assistant")
st.info(f"Currently viewing: {nav}")

# Feature 5.0: Proactive Triggers
check_proactive_triggers(current_page=nav)

# Layout
layout_col1, layout_col2 = st.columns([0.4, 0.6])

with layout_col1:
    render_avatar(
        state=st.session_state.kali_status,
        message=st.session_state.kali_message,
        confidence=get_confidence()
    )
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        if st.button("🎙️ Listen", use_container_width=True):
            st.session_state.kali_query = listen()
    with v_col2:
        mute_label = "🔇 Unmute" if st.session_state.kali_muted else "🔊 Mute"
        if st.button(mute_label, use_container_width=True):
            st.session_state.kali_muted = not st.session_state.kali_muted
            st.rerun()

with layout_col2:
    query = st.chat_input("Ask KALI anything...", key="kali_main_chat")
    
    if query or st.session_state.kali_query:
        final_query = query or st.session_state.kali_query
        st.session_state.kali_query = None
        st.session_state.kali_message = ""
        st.session_state.kali_status = "thinking"
        
        for token in ask_kali(final_query, context=nav):
            st.session_state.kali_message += token
        
        speak(st.session_state.kali_message)
        st.session_state.kali_status = "idle"
        st.rerun()

    st.header(nav)
    if nav == "KALI AVATAR CORE":
        run_avatar_specs()
        render_system_status()
    elif nav == "TECHNICAL REPORT (A1)":
        safe_run(a1.run_assignment_1)
    elif nav == "PORTFOLIO OPTIMIZER (A2)":
        safe_run(a2.run_assignment_2)
    elif nav == "THEORETICAL CONCEPTS":
        run_theoretical_info()
    elif nav == "PROJECT DOCUMENTATION":
        run_project_docs()

st.markdown("---")
st.caption("KALI — Quantum Computing Education Platform | Built with Streamlit")
