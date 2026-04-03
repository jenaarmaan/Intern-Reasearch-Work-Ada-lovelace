import streamlit as st
import sys
import os
import time

# Add Shared_AI_Avatar to path
sys.path.append(os.path.abspath("Shared_AI_Avatar"))
from avatar import render_ai_avatar

st.set_page_config(
    page_title="AI Avatar V2.0 - World-Class Evaluation",
    page_icon="🤖",
    layout="wide"
)

# Global Dark Override
st.markdown("""
<style>
    .stApp { background: #020205 !important; color: #e0e0e0 !important; }
    h1, h2, h3 { color: #00e5ff !important; font-family: 'Space Grotesk', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

st.title("💠 AI Avatar V2.0: World-Class Upgrade")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 🎛️ COGNITIVE CONTROLS")
    status_select = st.radio("Switch Processing Mode", ["Idle (Blue)", "Processing (Purple)", "Success (Green)"])
    status_map = {"Idle (Blue)": "idle", "Processing (Purple)": "processing", "Success (Green)": "success"}
    current_status = status_map[status_select]
    
    context_type = st.selectbox("Assign Research Domain", ["Assignment 1", "Assignment 2", "Portfolio Optimizer", "Mission Control"])
    custom_msg = st.text_input("Simulate AI Output", f"Awaiting instructions in {context_type} mode.")

    st.markdown("""
        <div style="background: rgba(0, 229, 255, 0.05); padding: 25px; border-radius: 20px; border: 1px solid rgba(0, 229, 255, 0.1); margin-top:30px;">
            <p style="color:#00e5ff; font-weight:bold; margin-bottom:10px;">🌟 ELITE UPGRADE LOG:</p>
            <ul style="font-size:0.9rem; line-height:1.6;">
                <li><strong>Dynamic Glow:</strong> Border and aura react to logic state.</li>
                <li><strong>Kinetic Typo:</strong> Messages appear via character-stream animation.</li>
                <li><strong>Laser Scan:</strong> Advanced biometric beam sweeps vertically.</li>
                <li><strong>Modular Logic:</strong> Plug this into any assignment with one line.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🤖 INTERFACE PREVIEW")
    render_ai_avatar(context=context_type, message=custom_msg, status=current_status)
    
    # Simulate a "Calculate" flow
    if st.button("🌟 INITIATE CROSS-ASSIGNMENT TASK SYNC"):
        with st.status("Performing Quantum Handshake...", expanded=True):
            render_ai_avatar(context=context_type, message="Initializing Qubits...", status="processing")
            time.sleep(1.5)
            st.success("Task Complete!")
            render_ai_avatar(context=context_type, message="Neural Optimization Successful.", status="success")

st.markdown("---")
st.markdown("<div style='text-align:center; opacity:0.5; font-size:0.8rem;'>ADA LOVELACE RESEARCH INSTITUTE | COGNITIVE INTERFACE DIVISION</div>", unsafe_allow_html=True)
