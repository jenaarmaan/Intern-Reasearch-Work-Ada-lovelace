import streamlit as st
import os
import base64

def get_base64_svg(path):
    # Ensure asset exists
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_avatar(state="idle", message=""):
    """
    Renders a clean, friendly KALI avatar with simple state-based animations.
    States: idle (blue), thinking (amber), speaking (green)
    """
    avatar_path = os.path.join("Shared_AI_Avatar", "assets", "kali_avatar.svg")
    
    # Map state to CSS class
    state_class = f"kali-{state}"
    
    # Status text based on page or activity
    current_topic_key = st.session_state.get("current_topic", None)
    topic_name = "Introduction"
    if current_topic_key:
        from quantum_curriculum import CURRICULUM
        topic_name = CURRICULUM[current_topic_key]['title']
        
    status_text = f"Exploring · {topic_name}"
    if state == "thinking": status_text = "Thinking..."
    if state == "speaking": status_text = "Explaining..."

    # Avatar & Status Layout
    st.markdown("<div class='kali-avatar-container'>", unsafe_allow_html=True)
    
    b64_avatar = get_base64_svg(avatar_path)
    
    st.markdown(f'''
        <div class="kali-avatar {state_class}">
            <img src="data:image/svg+xml;base64,{b64_avatar}" width="150" style="display: block; margin: 0 auto; border-radius: 50%;">
        </div>
        <div class="kali-status-label">{status_text}</div>
    ''', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Speech Bubble (No typewriter, just clean container)
    if message:
        st.markdown(f'''
            <div class="kali-speech-bubble">
                {message}
            </div>
        ''', unsafe_allow_html=True)

    # Simple Chat History (Expander)
    history = st.session_state.get("kali_history", [])
    if history:
        with st.expander("🗨️ Recent Chat (History)"):
            # Only show the last 5 relevant interactions
            for msg in history[-5:]:
                role = "👤 You" if msg['role'] == "user" else "🤖 KALI"
                st.markdown(f"**{role}**: {msg['content']}")

def render_system_status():
    """Simple status check for the KALI core."""
    st.sidebar.markdown("---")
    st.sidebar.caption("CORE STABILITY: NOMINAL")
    st.sidebar.caption("SYNCHRONIZATION: 100%")

def explain_chart(chart_title, data_summary):
    """Triggered by 'Ask KALI' button under charts."""
    # Simplified placeholder for chart analysis in educational mode
    st.info(f"KALI: In the context of {chart_title}, this data shows {data_summary}. Fascinating, right?")
