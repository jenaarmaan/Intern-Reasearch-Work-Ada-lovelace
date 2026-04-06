import streamlit as st
import sys
import os
import time

# --- PADDING NUCLEAR FIX (FIRST ACTION) ---
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

# --- Path Integration Hub ---
def add_path(folder):
    p = os.path.abspath(folder)
    if p not in sys.path: sys.path.append(p)

add_path("Shared_Core")
add_path("Shared_AI_Avatar")
add_path("Assignment_1")
add_path("Assignment_2")

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

# --- Import Components ---
from avatar import render_avatar, explain_chart
from theory_docs import run_theoretical_info, run_project_docs
from avatar_specs import run_avatar_specs
from kali_proactive import check_proactive_triggers, safe_run
from kali_brain import ask_kali, get_confidence
from kali_voice import listen, speak

import Assignment_1.app_module as a1
import Assignment_2.app_module as a2

# --- Page Config ---
st.set_page_config(
    page_title="KALI OS :: MISSION CONTROL",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.markdown("<h1 style='color:#00f2ff; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0, 242, 255, 0.4);'>KALI</h1><p style='font-size:0.4rem; letter-spacing:3px; opacity:0.7; font-weight:700;'>KINETIC AGENTIC LEARNING INTELLIGENCE</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🧬 SYSTEM NODES")
    nav = st.radio("Access Level", ["PORTFOLIO OPTIMIZER (A2)", "TECHNICAL REPORT (A1)", "KALI AVATAR CORE", "THEORETICAL CONCEPTS", "PROJECT DOCUMENTATION"])
    
    st.markdown("---")
    st.markdown("### 🛠️ KALI VOCABULARY")
    with st.expander("Hover for KALI Definitions"):
        st.button("Sharpe Ratio", help="KALI: The mathematical reward-to-variability ratio. Higher = More efficient evolution.", use_container_width=True)
        st.button("Ry-Gate", help="KALI: My primary quantum rotation actuator. It shifts our probability vectors toward the global optima.", use_container_width=True)
        st.button("PEAS Framework", help="KALI: My DNA—Performance, Environment, Actuators, Sensors. It's how I perceive and act.", use_container_width=True)
    
    st.markdown("---")
    st.info("KALI OS Status: **NOMINAL**")

# --- Persistent Persistence Layer (Header Section) ---
# Feature 5.0: Proactive Triggers
check_proactive_triggers(current_page=nav)

st.markdown("<div style='text-align:right;'><span class='status-capsule'>KALI NEXUS SYNC :: ONLINE [L-PK]</span></div>", unsafe_allow_html=True)

header_col1, header_col2 = st.columns([1.5, 2.5])

with header_col1:
    # Feature 2.0 & 6.0: KALI HUD & Avatar
    render_avatar(
        state=st.session_state.get("kali_status", "idle"),
        message=st.session_state.get("kali_message", "KALI Core Ready."),
        confidence=get_confidence()
    )
    
    # Feature 4.0: Voice Control HUD
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        if st.button("🎙️ LISTEN", use_container_width=True):
            transcription = listen()
            if transcription: st.session_state.kali_query = transcription
    with v_col2:
        mute_label = "🔇 UNMUTE" if st.session_state.get("kali_muted") else "🔊 MUTE"
        if st.button(mute_label, use_container_width=True):
            st.session_state.kali_muted = not st.session_state.get("kali_muted", False)
            st.rerun()

with header_col2:
    st.markdown(f"<p style='font-size:0.7rem; color:var(--neon-blue); letter-spacing:4px;'>MISSION MONITOR V5.2</p><h1 style='font-size: 3.5rem; margin-bottom:0;'>{nav}</h1><p style='font-size: 1.1rem; opacity: 0.7; letter-spacing: 1px;'>Unified Intelligence Portal :: KALI AI OS</p>", unsafe_allow_html=True)
    
    # Feature 6.2: Persistent KALI Chat Input
    user_query = st.chat_input("Transmit Command (Press K to focus)...", key="kali_chat_main_input")
    
    # If speech or text input exists, process it
    final_query = user_query or st.session_state.get("kali_query")
    if final_query:
        st.session_state.kali_status = "thinking"
        st.session_state.kali_query = None # Reset
        st.session_state.kali_message = ""
        # Process streaming output
        for token in ask_kali(final_query, context=nav):
            st.session_state.kali_message += token
        
        # After text finishes, speak it
        speak(st.session_state.kali_message)
        st.session_state.kali_status = "idle"
        st.rerun()

st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>")

# --- Content Hub ---
if nav == "TECHNICAL REPORT (A1)":
    safe_run(a1.run_assignment_1)
elif nav == "PORTFOLIO OPTIMIZER (A2)":
    safe_run(a2.run_assignment_2)
elif nav == "KALI AVATAR CORE":
    run_avatar_specs()
elif nav == "THEORETICAL CONCEPTS":
    run_theoretical_info()
elif nav == "PROJECT DOCUMENTATION":
    run_project_docs()

st.markdown("<br><br><br><div style='text-align:center; font-size:0.75rem; color:gray; opacity: 0.5; padding: 40px; border-top:1px solid rgba(255,255,255,0.03);'>KALI AI NETWORKS | KINETIC AGENTIC LEARNING INTELLIGENCE | ALL SYSTEMS NOMINAL</div>", unsafe_allow_html=True)
