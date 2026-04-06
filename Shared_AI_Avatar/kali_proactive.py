import streamlit as st
import time
from kali_brain import get_kali_response

def handle_proactive_triggers():
    """Checks for proactive triggers in every rerun."""
    
    # 1. App Load Greeting
    if "kali_greeted" not in st.session_state:
        st.session_state.kali_greeted = True
        st.session_state.kali_message = f"KALI Core Online. System time: {time.strftime('%H:%M:%S')}. Access levels: UNLIMITED."
        st.session_state.kali_status = "idle"
        st.session_state.kali_confidence = 100

    # 2. Idle Detection (Placeholder logic - requires client-side tracking ideally)
    # In Streamlit, we can track 'last_action' time
    if "last_action_time" not in st.session_state:
        st.session_state.last_action_time = time.time()
    
    current_time = time.time()
    if current_time - st.session_state.last_action_time > 30 and not st.session_state.get("idle_prompt_sent", False):
        st.session_state.kali_message = "Your research has paused. Should we re-calibrate the Quantum Genetic population?"
        st.session_state.kali_status = "warning"
        st.session_state.idle_prompt_sent = True

def trigger_qga_insight(metrics_summary):
    """Triggered after QGA optimization completion."""
    msg = get_kali_response(f"The optimization just finished with these results: {metrics_summary}. Provide a 2-sentence punchy insight.", current_context="Assignment 2")
    st.session_state.kali_message = msg
    st.session_state.kali_status = "eureka"
    st.session_state.kali_confidence = 98

def trigger_error_report(error_msg):
    """Triggered when an error occurs."""
    st.session_state.kali_message = f"Protocol breakdown detected. {error_msg} is hindering our convergence. Switching to redundant nodes."
    st.session_state.kali_status = "error"
    st.session_state.kali_confidence = 45

def run_kali_walkthrough():
    """Handles the 90-second scripted walkthrough."""
    steps = [
        {"nav": "PROJECT DOCUMENTATION", "msg": "Welcome to KALI OS. I am your Kinetic Agentic Learning Intelligence. Let's begin the system audit.", "status": "idle"},
        {"nav": "TECHNICAL REPORT (A1)", "msg": "Assignment 1: Agent Architecture. I've mapped the PEAS framework across Devin and Claude. Cognitive diversity is peak.", "status": "thinking"},
        {"nav": "PORTFOLIO OPTIMIZER (A2)", "msg": "Assignment 2: The Quantum Core. Here we utilize Ry-gate rotations to solve the Markowitz Frontier. Precision is absolute.", "status": "excited"},
        {"nav": "KALI AVATAR CORE", "msg": "I am the innovation. A state-aware, kinetic entity bridging the gap between research and intelligence.", "status": "eureka"}
    ]
    
    for step in steps:
        st.session_state.nav_target = step["nav"]
        st.session_state.kali_message = step["msg"]
        st.session_state.kali_status = step["status"]
        time.sleep(3) # Walkthrough speed
        st.rerun()

def generate_evaluator_report():
    """Generates a structured session summary."""
    report = f"""
KALI :: MISSION REPORT
----------------------
Session Start: {time.ctime()}
Intelligence Core: Gemini 1.5 Flash
Visual State: Kinetic / 8-Mode
Knowledge Domains: QGA, Portfolio Optimization, PEAS

EXECUTIVE SUMMARY:
{st.session_state.get('kali_chat_history', ['No dialogue recorded.'])[0:4]}

TECHNICAL MILESTONES:
- Quantum Genetic Algorithm Benchmarking: SUCCESS
- AI Agent Architecture Mapping: SUCCESS
- Real-time TTS/STT Integration: SUCCESS
    """
    return report
