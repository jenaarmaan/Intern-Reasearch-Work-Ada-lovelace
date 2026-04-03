import streamlit as st
import sys
import os
import time

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

# Unified Navigation Hub - Direct imports for modules
import Assignment_1.app_module as a1
import Assignment_2.app_module as a2

# --- Page Config ---
st.set_page_config(
    page_title="AI MISSION CONTROL v3.0",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Space+Grotesk:wght@300;400;700&display=swap');
    
    .stApp { background: radial-gradient(circle at 50% 10%, #0d0e23, #020205); color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: 1px; }
    
    section[data-testid="stSidebar"] { background: rgba(5, 6, 15, 0.95) !important; backdrop-filter: blur(30px); border-right: 1px solid rgba(255,255,255,0.05); }
    .status-capsule { background: rgba(0, 229, 255, 0.1); padding: 5px 12px; border-radius: 20px; border: 1px solid rgba(0, 229, 255, 0.4); font-size: 0.7rem; color: #00e5ff; }
</style>
""", unsafe_allow_html=True)

# --- Navigation ---
with st.sidebar:
    st.markdown("<h1 style='color:#00e5ff; margin-bottom:0;'>ADA LOVELACE</h1><p style='font-size:0.6rem; letter-spacing:4px; opacity:0.5;'>UNIFIED RESEARCH OS</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🧭 NAVIGATION NEXUS")
    nav = st.radio("Access Level", ["BEE DASHBOARD (A2)", "PORTFOLIO OPTIMIZER (A1)", "THEORETICAL CONCEPTS", "PROJECT DOCUMENTATION"])
    
    st.markdown("---")
    st.write("**📡 CONNECTION:** 🟢 STABLE")
    st.write("**🧠 SYSTEM CORE:** QGA.V3-PRO")

# --- Header ---
st.markdown("<div style='text-align:right;'><span class='status-capsule'>SATELLITE ACTIVE :: L-PK :: 0.4ms</span></div>", unsafe_allow_html=True)

# Avatar persistence
avatar_col1, avatar_col2 = st.columns([1, 2.5])
with avatar_col1:
    status_map = {
        "BEE DASHBOARD (A2)": ("BEE V3.0 initializing... Ready for strategy.", "idle"),
        "PORTFOLIO OPTIMIZER (A1)": ("Portfolio Optimizer Alpha is online. Select your assets.", "idle"),
        "THEORETICAL CONCEPTS": ("Displaying Quantum GA theoretical structures.", "idle"),
        "PROJECT DOCUMENTATION": ("Analyzing Project Metadata. Guidelines extracted.", "idle")
    }
    msg, stat = status_map[nav]
    render_ai_avatar(context=nav.split()[-1], message=msg, status=stat)

with avatar_col2:
    st.markdown(f"<div style='margin-top:20px;'><h1 style='margin-bottom:0; color:#00e5ff;'>{nav}</h1><p style='opacity:0.6;'>Mission Control Hub Integration Active.</p></div>", unsafe_allow_html=True)

st.markdown("---")

# --- Page Selection ---
if nav == "PORTFOLIO OPTIMIZER (A1)":
    a1.run_assignment_1()
elif nav == "BEE DASHBOARD (A2)":
    a2.run_assignment_2()
elif nav == "THEORETICAL CONCEPTS":
    run_theoretical_info()
elif nav == "PROJECT DOCUMENTATION":
    run_project_docs()

# --- Footer ---
st.markdown("<br><br><br><div style='text-align:center; font-size:0.7rem; color:gray; border-top:1px solid rgba(255,255,255,0.05); padding-top:20px;'>ADA LOVELACE RESEARCH INSTITUTE | UNIFIED MISSION CONTROL | V3.2.1-NEXUS</div>", unsafe_allow_html=True)
