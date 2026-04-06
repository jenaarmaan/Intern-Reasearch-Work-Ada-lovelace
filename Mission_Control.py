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
    page_title="KALI OS :: MISSION CONTROL",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PADDING NUCLEAR FIX & SCANLINES & CSS LOAD ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("Shared_AI_Avatar/style.css")

st.markdown("""
    <style>
        [data-testid="stHeader"] {display: none !important;}
        .block-container {padding-top: 0rem !important; padding-bottom: 0rem !important; margin-top: -2.5rem !important;}
        .stAppDeployButton {display:none !important;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stMain { margin-top: 0px !important; padding-top: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# Navigation Nexus
with st.sidebar:
    st.markdown("<h1 style='color:#00f2ff; font-size: 2.2rem; text-shadow: 0 0 20px rgba(0, 242, 255, 0.4); letter-spacing:0.15em;'>KALI</h1><p style='font-size:0.45rem; letter-spacing:4px; opacity:0.8; font-weight:700; margin-bottom:40px;'>KINETIC AGENTIC LEARNING INTELLIGENCE</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-section-header'>SYSTEM NODES</div>", unsafe_allow_html=True)
    nav_options = {
        "PORTFOLIO OPTIMIZER (A2)": "teal",
        "TECHNICAL REPORT (A1)": "gray",
        "KALI AVATAR CORE": "red",
        "THEORETICAL CONCEPTS": "gray",
        "PROJECT DOCUMENTATION": "gray"
    }
    nav = st.radio("Access Level", list(nav_options.keys()), label_visibility="collapsed")
    
    st.markdown("<div class='sidebar-section-header'>COGNITIVE CONTROLS</div>", unsafe_allow_html=True)
    if st.button("🚀 SYNC WALKTHROUGH", use_container_width=True):
        run_kali_walkthrough()
    
    st.markdown("<div class='sidebar-section-header'>KALI VOCABULARY</div>", unsafe_allow_html=True)
    with st.expander("Hover for AI Glossary"):
        st.button("Sharpe Ratio", help="KALI: The mathematical reward-to-variability ratio.", use_container_width=True)
        st.button("Ry-Gate", help="KALI: My primary quantum rotation actuator.", use_container_width=True)
    
    st.markdown("---")
    status_pulse = "nominal" if st.session_state.kali_status == "idle" else "alert"
    st.markdown(f"<div class='status-capsule-{status_pulse}'>KALI OS STATUS :: {st.session_state.kali_status.upper()}</div>", unsafe_allow_html=True)

# Top Header Bar
header_html = f"""
<div class="mission-header-v52">
    <div class="header-left">MISSION MONITOR V5.2</div>
    <div class="header-center">NEXUS_BREADCRUMB :: {nav}</div>
    <div class="header-right">
        <span class="nexus-sync-pill">KALI NEXUS SYNC :: ONLINE <span class="sync-dot"></span></span>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# Feature 5.0: Proactive Triggers
check_proactive_triggers(current_page=nav)

# Layout
layout_col1, layout_col2, layout_col3 = st.columns([0.15, 0.45, 0.40])

with layout_col2:
    render_avatar(
        state=st.session_state.kali_status,
        message=st.session_state.kali_message,
        confidence=get_confidence()
    )
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        if st.button("🎙️ LISTEN", use_container_width=True):
            st.session_state.kali_query = listen()
    with v_col2:
        mute_label = "🔇 UNMUTE" if st.session_state.kali_muted else "🔊 MUTE"
        if st.button(mute_label, use_container_width=True):
            st.session_state.kali_muted = not st.session_state.kali_muted
            st.rerun()

with layout_col3:
    query = st.chat_input("TRANSMIT COMMAND [ PRESS K TO SCAN ]...", key="kali_main_chat")
    
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

    st.markdown(f"## {nav}")
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

st.markdown("<br><br><br><div style='text-align:center; font-size:0.75rem; color:gray; opacity: 0.5;'>KALI AI NETWORKS | ALL SYSTEMS NOMINAL</div>", unsafe_allow_html=True)
