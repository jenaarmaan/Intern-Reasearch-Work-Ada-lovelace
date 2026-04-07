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
    from kali_permissions import render_permission_sidebar, get_permission_pill
except ImportError as e:
    st.error(f"KALI System Node Sync Failure: {e}")
    st.stop()

import Assignment_1.app_module as a1
import Assignment_2.app_module as a2

from quantum_curriculum import CURRICULUM
from quiz_engine import render_quiz

# --- KALI Session Initialization ---
def init_kali_session():
    """Ensures KALI's cognitive states are initialized in the correct order."""
    if "kali_status" not in st.session_state: st.session_state.kali_status = "idle"
    if "kali_message" not in st.session_state: 
        st.session_state.kali_message = "Hello! I am KALI, your quantum computing guide. Which topic would you like to explore today?"
    if "kali_query" not in st.session_state: st.session_state.kali_query = None
    if "kali_muted" not in st.session_state: st.session_state.kali_muted = False
    if "last_interaction" not in st.session_state: st.session_state.last_interaction = time.time()
    if "kali_history" not in st.session_state: st.session_state.kali_history = []
    if "kali_best_sharpe" not in st.session_state: st.session_state.kali_best_sharpe = 0.0
    if "kali_ready" not in st.session_state: st.session_state.kali_ready = False
    
    # Curriculum State
    if "current_topic" not in st.session_state: st.session_state.current_topic = None
    if "topic_progress" not in st.session_state: 
        st.session_state.topic_progress = {k: "gray" for k in CURRICULUM.keys()} # gray, blue, green

init_kali_session()

# --- Page Config ---
st.set_page_config(
    page_title="Quantum Learning with KALI",
    page_icon="⚛️",
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
    st.caption("Your Quantum Computing Teacher")
    
    # Learning Progress Header
    completed = list(st.session_state.topic_progress.values()).count("green")
    st.sidebar.markdown(f"**Learning Progress:** {completed}/{len(CURRICULUM)} Topics")
    st.sidebar.progress(completed / len(CURRICULUM))
    
    st.sidebar.header("🎓 Curriculum")
    
    # Topic Selector Logic
    selected_topic_key = None
    for key, topic in CURRICULUM.items():
        dot_color = st.session_state.topic_progress[key]
        emoji = "⚪" if dot_color == "gray" else "🔵" if dot_color == "blue" else "🟢"
        if st.sidebar.button(f"{emoji} {topic['title']}", key=f"btn_{key}", use_container_width=True):
            selected_topic_key = key
            st.session_state.current_topic = key
            st.session_state.topic_progress[key] = "blue"
            st.session_state.nav_portal = "QUANTUM LEARNING HOME" # Force nav sync
            st.session_state.kali_message = topic['explanation'].split('.')[0] + "." # First sentence
            st.session_state.kali_status = "idle"
            st.rerun()

    # Navigation Controller Sync
    if "nav_portal" not in st.session_state:
        st.session_state.nav_portal = "QUANTUM LEARNING HOME"
    
    nav_options = {
        "QUANTUM LEARNING HOME": "teal",
        "PORTFOLIO OPTIMIZER (A2)": "gray",
        "TECHNICAL REPORT (A1)": "gray",
        "KALI AVATAR CORE": "red",
        "THEORETICAL CONCEPTS": "gray",
        "PROJECT DOCUMENTATION": "gray"
    }
        
    nav = st.radio("Select Portal", list(nav_options.keys()), 
                   index=list(nav_options.keys()).index(st.session_state.nav_portal),
                   key="portal_selector", label_visibility="collapsed")
    
    # Sync radio back to state
    st.session_state.nav_portal = nav
    
    # Feature 4.0: Permission Sidebar
    render_permission_sidebar()
    
    st.sidebar.header("AI Glossary")
    with st.expander("Terms"):
        st.button("Qubit", help="The basic unit of quantum information.", use_container_width=True)
        st.button("Entanglement", help="A spooky connection between particles.", use_container_width=True)
    
    st.markdown("---")
    status_type = "nominal" if st.session_state.kali_status == "idle" else "alert"
    st.markdown(f"<div class='status-capsule status-{status_type}'>STATUS: {st.session_state.kali_status.upper()}</div>", unsafe_allow_html=True)

# Main Header
h_col1, h_col2 = st.columns([0.8, 0.2])
with h_col1:
    # Feature: Dynamic Header Title
    if nav == "PORTFOLIO OPTIMIZER (A2)":
        st.title("BEE Portfolio Optimizer")
    elif nav == "TECHNICAL REPORT (A1)":
        st.title("Comparative Research Report")
    else:
        st.title("Quantum Learning with KALI")
with h_col2:
    st.markdown(f"<div style='text-align: right; padding-top: 25px;'>{get_permission_pill('voice')}</div>", unsafe_allow_html=True)

# Feature 5.0: Proactive Triggers
check_proactive_triggers(current_page=nav)

# Layout: Widened main content area for Plots
layout_col1, layout_col2 = st.columns([0.3, 0.7])

with layout_col1:
    render_avatar(
        state=st.session_state.kali_status,
        message=st.session_state.kali_message
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
    
    # --- Feature 8: Stable Chat UI ---
    st.markdown("---")
    chat_container = st.container(height=300)
    with chat_container:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

# Processing Loop (Outside columns to allow rerun to refresh state)
if st.session_state.kali_status == "thinking":
    with st.spinner("KALI is thinking..."):
        # Get response from stable LLM brain
        last_user_msg = st.session_state.chat_history[-1]["content"]
        response = ask_kali(last_user_msg)
        
        # Update history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Manage history cap (10 exchanges = 20 messages)
        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[-20:]
            
        st.session_state.kali_message = response
        st.session_state.kali_status = "speaking"
        speak(response)
        st.session_state.kali_status = "idle"
        st.rerun()

with layout_col2:
    if nav == "QUANTUM LEARNING HOME":
        if st.session_state.current_topic:
            topic = CURRICULUM[st.session_state.current_topic]
            st.header(topic['title'])
            st.write(topic['explanation'])
            st.info(f"🇮🇳 **Indian Research Insight:** {topic['india_example']}")
            
            with st.expander("📝 Key Terms for this Lesson"):
                for item in topic['key_terms']:
                    st.write(f"- **{item['term']}**: {item['definition']}")
            
            # Render the interactive quiz using the centralized engine
            render_quiz(st.session_state.current_topic)
            
            # Final lesson footer fact
            st.markdown("---")
            st.caption(f"💡 {topic['fact']}")
            
        else:
            st.subheader("Welcome to Your Quantum Journey!")
            st.write("I am KALI, and I'm here to help you master the fundamentals of quantum computing. Choose a topic from the curriculum sidebar to begin our first lesson.")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Bloch_sphere.svg/1200px-Bloch_sphere.svg.png", caption="The Bloch Sphere: Visualizing a Qubit's possibilities.", width=400)

    elif nav == "KALI AVATAR CORE":
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
st.caption("KALI — Quantum Computing Education Platform | Built for National Quantum Mission Research Awareness")

# Global Chat Input (Pinned to bottom for stability)
query = st.chat_input("Ask KALI about quantum computing...")

if query or st.session_state.kali_query:
    final_query = query or st.session_state.kali_query
    st.session_state.kali_query = None
    
    # Add to history
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": "user", "content": final_query})
    
    st.session_state.kali_status = "thinking"
    st.session_state.kali_message = "KALI is analyzing your query..."
    st.rerun()
