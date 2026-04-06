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

# --- Import Components ---
from avatar import render_ai_avatar
from theory_docs import run_theoretical_info, run_project_docs
from avatar_specs import run_avatar_specs
from kali_proactive import run_kali_walkthrough, generate_evaluator_report

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
    
    :root { --neon-blue: #00f2ff; --neon-purple: #bc13fe; }
    .stApp { background: radial-gradient(circle at 50% 10%, #0d0e23, #020205); color: #e0e0e0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; background: linear-gradient(135deg, white 0%, #00f2ff 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
    section[data-testid="stSidebar"] { background: rgba(4, 5, 12, 0.98) !important; backdrop-filter: blur(40px); border-right: 1px solid rgba(0, 242, 242, 0.15); }
    .status-capsule { background: rgba(0, 242, 255, 0.08); padding: 8px 18px; border-radius: 50px; border: 1px solid rgba(0, 242, 242, 0.4); font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: #00f2ff; text-transform: uppercase; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

# --- Navigation Nexus ---
with st.sidebar:
    st.markdown("<h1 style='color:#00f2ff; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0, 242, 255, 0.4);'>KALI</h1><p style='font-size:0.4rem; letter-spacing:3px; opacity:0.7; font-weight:700;'>KINETIC AGENTIC LEARNING INTELLIGENCE</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🧬 SYSTEM NODES")
    nav = st.radio("Access Level", ["PORTFOLIO OPTIMIZER (A2)", "TECHNICAL REPORT (A1)", "KALI AVATAR CORE", "THEORETICAL CONCEPTS", "PROJECT DOCUMENTATION"])
    
    st.markdown("---")
    st.markdown("### 🛠️ COGNITIVE CONTROLS")
    
    # Competition / Demo Mode
    if st.button("🚀 INITIATE DEMO WALKTHROUGH"):
        run_kali_walkthrough()
        
    # Evaluator Report
    report_text = generate_evaluator_report()
    st.download_button("📄 GENERATE EVALUATOR REPORT", data=report_text, file_name="KALI_Mission_Report.txt")
    
    st.markdown("---")
    st.info("KALI OS Status: **NOMINAL**")

# --- Persistent Persistence Layer (Header Section) ---
st.markdown("<div style='text-align:right;'><span class='status-capsule'>KALI NEXUS SYNC :: ONLINE [L-PK]</span></div>", unsafe_allow_html=True)

header_col1, header_col2 = st.columns([1.5, 2.5])

with header_col1:
    # Context Selection for Avatar
    current_ctx = nav.split()[-1]
    render_ai_avatar(context=current_ctx)

with header_col2:
    # Feature 2.3 & 2.4: Google-Tier Geometric Branding
    st.markdown(f"<div style='margin-top:0px;'><p style='font-size:0.7rem; color:var(--neon-blue); letter-spacing:4px;'>MISSION MONITOR V5.2</p><h1 style='font-size: 3.5rem; margin-bottom:0;'>{nav}</h1><p style='font-size: 1.1rem; opacity: 0.7; letter-spacing: 1px;'>Unified Intelligence Portal :: KALI AI OS</p></div>", unsafe_allow_html=True)
    
    # Persistent Chat Hint
    st.caption("Press 'K' to focus command input at any time.")

st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>")

# --- Content Hub ---
if nav == "TECHNICAL REPORT (A1)":
    a1.run_assignment_1()
elif nav == "PORTFOLIO OPTIMIZER (A2)":
    a2.run_assignment_2()
elif nav == "KALI AVATAR CORE":
    run_avatar_specs()
elif nav == "THEORETICAL CONCEPTS":
    run_theoretical_info()
elif nav == "PROJECT DOCUMENTATION":
    run_project_docs()

st.markdown("<br><br><br><div style='text-align:center; font-size:0.75rem; color:gray; opacity: 0.5; padding: 40px; border-top:1px solid rgba(255,255,255,0.03);'>KALI AI NETWORKS | KINETIC AGENTIC LEARNING INTELLIGENCE | ALL SYSTEMS NOMINAL</div>", unsafe_allow_html=True)
