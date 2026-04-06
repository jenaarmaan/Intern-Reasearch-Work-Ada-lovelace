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

add_path("Shared_Core")
add_path("Shared_AI_Avatar")
add_path("Assignment_1")
add_path("Assignment_2")

# --- Import Components ---
# These imports rely on the paths added above
from avatar import render_avatar, explain_chart
from theory_docs import run_theoretical_info, run_project_docs
from avatar_specs import run_avatar_specs
from kali_proactive import check_proactive_triggers, safe_run, run_kali_walkthrough
from kali_brain import ask_kali, get_confidence
from kali_voice import listen, speak

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

init_kali_session()

# --- Page Config ---
st.set_page_config(
    page_title="KALI OS :: MISSION CONTROL",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PADDING NUCLEAR FIX & SCANLINES ---
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

# --- Google-Level Global Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root { 
        --neon-blue: #00f2ff; 
        --neon-purple: #bc13fe; 
        --glass-bg: rgba(10, 11, 25, 0.45);
    }
    
    .stApp { 
        background: radial-gradient(circle at 50% 10%, #0d0e23, #020205); 
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Premium Scanline Overlay */
    .stApp::after {
        content: " ";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 4px, 3px 100%;
        pointer-events: none;
        z-index: 1000;
        opacity: 0.25;
    }

    h1, h2, h3 { 
        font-family: 'Space Grotesk', sans-serif !important; 
        background: linear-gradient(135deg, white 0%, #00f2ff 100%); 
        -webkit-background-clip: text; 
        background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }

    section[data-testid="stSidebar"] { 
        background: rgba(4, 5, 12, 0.98) !important; 
        backdrop-filter: blur(40px); 
        border-right: 1px solid rgba(0, 242, 242, 0.15); 
    }

    .status-capsule { 
        background: rgba(0, 242, 255, 0.08); 
        padding: 5px 14px; 
        border-radius: 50px; 
        border: 1px solid rgba(0, 242, 242, 0.3); 
        font-size: 0.65rem; 
        font-family: 'JetBrains Mono', monospace; 
        color: #00f2ff; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Navigation Nexus ---
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
    
    # Custom Radio with Coded Dots
    nav = st.radio("Access Level", list(nav_options.keys()), label_visibility="collapsed")
    
    st.markdown("<div class='sidebar-section-header'>COGNITIVE CONTROLS</div>", unsafe_allow_html=True)
    if st.button("🚀 SYNC WALKTHROUGH", use_container_width=True):
        run_kali_walkthrough()
    
    st.markdown("<div class='sidebar-section-header'>KALI VOCABULARY</div>", unsafe_allow_html=True)
    with st.expander("Hover for AI Glossary"):
        st.button("Sharpe Ratio", help="KALI: The mathematical reward-to-variability ratio. Higher = More efficient evolution.", use_container_width=True)
        st.button("Ry-Gate", help="KALI: My primary quantum rotation actuator. It shifts our probability vectors toward the global optima.", use_container_width=True)
    
    st.markdown("---")
    status_pulse = "nominal" if st.session_state.kali_status == "idle" else "alert"
    st.markdown(f"<div class='status-capsule-{status_pulse}'>KALI OS STATUS :: {st.session_state.kali_status.upper()}</div>", unsafe_allow_html=True)

# --- Top Header Bar ---
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

# Feature 6.0: Keyboard Tooltip & K-Shortcut Support
st.markdown("""
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    if (e.key.toLowerCase() === 'k') {
        const input = doc.querySelector('textarea[data-testid="stChatInputTextArea"]');
        if (input) input.focus();
    }
});
</script>
""", unsafe_allow_html=True)

# --- Main Layout (3 Columns: 15 / 45 / 40) ---
layout_col1, layout_col2, layout_col3 = st.columns([0.15, 0.45, 0.40])

with layout_col1:
    st.empty() # Gutter for sidebar transitions

with layout_col2:
    # Feature 2.0 & 6.0: KALI HUD & Avatar
    render_avatar(
        state=st.session_state.get("kali_status", "idle"),
        message=st.session_state.get("kali_message", "KALI Core Ready."),
        confidence=get_confidence()
    )
    
    # Feature 4.0: Voice Controls
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        if st.button("🎙️ LISTEN", use_container_width=True):
             from kali_voice import listen; st.session_state.kali_query = listen()
    with v_col2:
        mute_label = "🔇 UNMUTE" if st.session_state.kali_muted else "🔊 MUTE"
        if st.button(mute_label, use_container_width=True):
            st.session_state.kali_muted = not st.session_state.kali_muted
            st.rerun()

with layout_col3:
    # Feature 6.2: Persistent KALI Chat Input
    query = st.chat_input("TRANSMIT COMMAND [ PRESS K TO SCAN ]...", key="kali_main_chat")
    
    if query or st.session_state.kali_query:
        final_query = query or st.session_state.kali_query
        st.session_state.kali_query = None
        st.session_state.kali_message = ""
        
        for token in ask_kali(final_query, context=nav):
            st.session_state.kali_message += token
        
        from kali_voice import speak; speak(st.session_state.kali_message)
        st.session_state.kali_status = "idle"
        st.rerun()

    st.markdown(f"## {nav}")
    
    # Page Routing
    if nav == "KALI AVATAR CORE":
        from avatar import render_system_status
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

st.markdown("<br><br><br><div style='text-align:center; font-size:0.75rem; color:gray; opacity: 0.5; padding: 40px; border-top:1px solid rgba(255,255,255,0.03);'>KALI AI NETWORKS | KINETIC AGENTIC LEARNING INTELLIGENCE | ALL SYSTEMS NOMINAL</div>", unsafe_allow_html=True)
