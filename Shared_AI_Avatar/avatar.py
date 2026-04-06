import streamlit as st
import os
import base64
import time
from kali_brain import get_kali_response, stream_kali_typing
from kali_voice import speak_text
from kali_proactive import handle_proactive_triggers, trigger_error_report

# --- KALI Constants ---
AVATAR_DIR = os.path.dirname(__file__)

def get_base64_img(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def render_ai_avatar(context="General Research"):
    """
    KALI CORE :: Advanced Kinetic AI Avatar Renderer (V5.2)
    Now featuring multi-modal intelligence and proactive logic.
    """
    
    # 1. Initialize Session States for KALI
    if "kali_message" not in st.session_state:
        st.session_state.kali_message = "KALI Core Ready. Initiate research nodes."
    if "kali_status" not in st.session_state:
        st.session_state.kali_status = "idle"
    if "kali_confidence" not in st.session_state:
        st.session_state.kali_confidence = 100
    if "kali_history_log" not in st.session_state:
        st.session_state.kali_history_log = []
    if "kali_mute" not in st.session_state:
        st.session_state.kali_mute = False
        
    # 2. Inject Cognitive Design System (CSS)
    css_path = os.path.join(AVATAR_DIR, "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # 3. Load Avatar Asset (Holographic Neural Orb)
    asset_path = os.path.join(AVATAR_DIR, "assets", "premium_avatar.png")
    b64_img = get_base64_img(asset_path)
    img_tag = f'<img src="data:image/png;base64,{b64_img}" alt="KALI">' if b64_img else '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3N2NncwZ3JtcmN0Ym15bm15bm15bm15bm15bm1/l0HlRnAWXjnBYQV7W/giphy.gif" alt="KALI Offline">'

    # 4. Handle Proactive Triggers (App Load, Idle detection etc)
    handle_proactive_triggers()
    
    # 5. UI Layout - The KALI Panel
    with st.container():
        # Outer Class for states (idle, thinking, etc.)
        status_class = f"status-{st.session_state.kali_status}"
        
        # HTML RENDER
        st.markdown(f"""
        <div class="avatar-container {status_class}">
            <div class="particle-drift"></div>
            <div class="avatar-orb">
                <div class="orb-pulse"></div>
                {img_tag}
            </div>
            <div class="status-label">{st.session_state.kali_status} mode :: sync active</div>
            
            <!-- Typewriter Speech Bubble -->
            <div id="kali-speech-root" class="ai-speech-bubble">
                <p style="font-size:0.6rem; color:var(--kali-blue); font-family:'JetBrains Mono'; margin-bottom:8px; opacity:0.6;">
                    >> KALI_OS::{context.upper()} // L-PK
                </p>
                <div id="kali-text-placeholder">
                    <span class="kinetic-reveal">{st.session_state.kali_message}</span>
                    <span class="caret-pulse"></span>
                </div>
            </div>
            
            <!-- Confidence Meter -->
            <div class="confidence-bar-container">
                <div class="confidence-fill" style="width: {st.session_state.kali_confidence}%;"></div>
            </div>
            <p style="font-size:0.55rem; color:gray; text-align:right; margin-top:5px;">CONFIDENCE: {st.session_state.kali_confidence}%</p>
            
            <!-- Micro-Log -->
            <div class="micro-log">
                {''.join([f'<div>- {log}</div>' for log in st.session_state.kali_history_log[-5:]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 6. Interaction Controls (Mute/Chat/Voice)
        col_mute, col_voice, col_input = st.columns([1, 1, 6])
        
        with col_mute:
            if st.button("🔇" if st.session_state.kali_mute else "🔊"):
                st.session_state.kali_mute = not st.session_state.kali_mute
                st.rerun()
                
        with col_voice:
            # Placeholder for voice input via streamlit-audiorecorder
            # In real usage, st_audiorecorder() would go here
            st.button("🎙️")

        with col_input:
            chat_input = st.text_input("Transmit Command...", placeholder="Ask KALI about QGA or Portfolio Optimization", key="kali_chat_input", label_visibility="collapsed")
            
            # Simple Keyboard Shortcut handling (K to focus via streamlit usually needs JS or hacky methods)
            
        # 7. Response Logic (Brain + Voice + Typewriter)
        if chat_input and chat_input != st.session_state.get("last_chat", ""):
            st.session_state.last_chat = chat_input
            st.session_state.kali_status = "thinking"
            st.rerun() # Shift to thinking immediately

    # Thinking Transition (Processing response)
    if st.session_state.kali_status == "thinking":
        response = get_kali_response(st.session_state.kali_chat_input, current_context=context)
        st.session_state.kali_message = response
        st.session_state.kali_status = "speaking"
        st.session_state.kali_history_log.append(response)
        st.rerun()

    # Speaking Transition (Actioning speech/typewriter)
    if st.session_state.kali_status == "speaking":
        # Note: In Streamlit, rendering speech and typewriter simultaneously is tricky.
        # We start the speech-audio hidden while the typewriter reveals text.
        speak_text(st.session_state.kali_message, st.empty())
        # Placeholder for streaming typewriter (requires a specific UI container)
        # For simplicity in this demo, we'll reset status to idle after speech.
        time.sleep(2) # Mocking speech duration
        st.session_state.kali_status = "idle"
        st.rerun()

def explain_this(component_name, data_summary):
    """Triggered by 'Explain This' buttons below charts."""
    st.session_state.kali_status = "thinking"
    st.session_state.kali_message = get_kali_response(f"Explain this {component_name} in 2 witty sentences: {data_summary}")
    st.session_state.kali_status = "speaking"
    st.rerun()
