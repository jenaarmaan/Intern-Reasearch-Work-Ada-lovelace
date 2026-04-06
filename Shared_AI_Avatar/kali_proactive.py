import streamlit as st
import time
import random
from datetime import datetime
from kali_brain import ask_kali

# --- PROACTIVE CONFIG ---
IDLE_THRESHOLD = 30 # seconds
PROACTIVE_COOLDOWN = 120 # seconds before KALI nudges again

def get_time_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good morning."
    if hour < 18: return "Good afternoon."
    return "Good evening."

def on_optimization_complete(result_dict):
    """Triggered after QGA runs. Evaluates the Sharpe ratio and generates a response."""
    current_sharpe = result_dict.get('sharpe', 0)
    best_sharpe = st.session_state.get('kali_best_sharpe', 0)
    
    # Update Best Sharpe logic
    if current_sharpe > best_sharpe:
        st.session_state.kali_best_sharpe = current_sharpe
        st.session_state.kali_status = "excited"
        msg = f"Incredible. This new portfolio evolution achieved a Sharpe ratio of {current_sharpe:.2f}, surpassing our previous benchmark. Convergence is nearly 100%."
    else:
        st.session_state.kali_status = "eureka"
        # Generate 2-sentence insight using KALI's brain
        query = f"The QGA optimization is complete with a Sharpe of {current_sharpe:.2f}. Give a witty 2-sentence insight."
        msg = "".join(list(ask_kali(query, context="A2")))
        
    st.session_state.kali_message = msg
    st.session_state.last_interaction = time.time()
    st.rerun()

def safe_run(func, *args, **kwargs):
    """A wrapper to catch errors and use KALI to explain them simply."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.session_state.kali_status = "error"
        query = f"An error occurred in your systems: {str(e)}. Explain what happened in one simple, witty sentence as KALI."
        explanation = "".join(list(ask_kali(query, context="General")))
        st.session_state.kali_message = f"Critical Alert: {explanation}"
        st.session_state.last_interaction = time.time()
        # Log error for devs
        print(f"KALI TRAPPED ERROR: {e}")
        st.rerun()

def check_proactive_triggers(current_page="Home"):
    """Main loop called from Mission_Control on every rerun."""
    
    now = time.time()
    
    # 1. Boot Greeting (First Load)
    if "kali_booted" not in st.session_state:
        st.session_state.kali_booted = True
        greeting = get_time_greeting()
        st.session_state.kali_message = f"{greeting} KALI Core Online. Quantum systems are synchronized. What are we solving today?"
        st.session_state.last_interaction = now
        st.session_state.kali_current_page = current_page
        return

    # 2. Module Change Detection
    prev_page = st.session_state.get("kali_current_page", "Home")
    if current_page != prev_page:
        st.session_state.kali_current_page = current_page
        orientations = {
            "TECHNICAL REPORT (A1)": "Navigating to Asset A1. We're looking at the QGA Stock Portfolio Logic nodes.",
            "PORTFOLIO OPTIMIZER (A2)": "Sector A2 accessed. The dynamic Portfolio Optimizer is live. What's our risk-weighted target?",
            "KALI AVATAR CORE": "Mirroring cognitive systems. You're inside my architectural specs now.",
            "THEORETICAL CONCEPTS": "Entering the Knowledge Vault. Ry-gate proofs and Markowitz derivations are ready.",
            "PROJECT DOCUMENTATION": "System Logs Node. All architecture maps are here for your review."
        }
        st.session_state.kali_message = orientations.get(current_page, f"Orientation Update: Viewing {current_page}.")
        st.session_state.last_interaction = now
        st.session_state.kali_status = "idle"
        return

    # 3. Idle Detection (Nudges after inactivity)
    time_since_last = now - st.session_state.get("last_interaction", now)
    last_nudge = st.session_state.get("kali_last_nudge", 0)
    
    if time_since_last > IDLE_THRESHOLD and (now - last_nudge) > PROACTIVE_COOLDOWN:
        st.session_state.kali_last_nudge = now
        nudges = [
            "Still there? The quantum matrix is idling. Should we run a new optimization?",
            "System entropy is increasing. Perhaps we should review the Portfolio weights in A2?",
            "KALI is standing by. Give me a command or let's look at some agent logic.",
            "Waiting for mission input. The efficient frontier isn't going to chart itself."
        ]
        st.session_state.kali_message = random.choice(nudges)
        st.session_state.kali_status = "warning"
        # We don't rerun here to avoid infinite loops, just update msg for next render
