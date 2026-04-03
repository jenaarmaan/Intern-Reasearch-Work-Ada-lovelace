import streamlit as st
import os
import base64
import functools

# --- ELITE CACHING PROTOCOL (V4.1) ---
@st.cache_resource
def get_base64_image(image_path):
    """Caches base64 string to prevent costly disk I/O during reruns."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def highlight_keywords(text):
    """Automatically highlights elite KALI keywords for a premium synthetic feel."""
    keywords = ["KALI", "Quantum", "Mission Control", "Success", "Analyzing", "Optimizing", "Genetic", "Autonomous", "Devin", "Claude"]
    for word in keywords:
        text = text.replace(word, f"<b>{word}</b>")
    return text

def render_ai_avatar(context="General Research", message="Status nominal.", status="idle"):
    """
    Elite KALI AI Avatar Renderer - V4.1 (Cognitive Intelligence)
    """
    
    # Injection: Loading Elite Design System
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Resource: High-res avatar asset (Cached)
    avatar_asset = os.path.join(os.path.dirname(__file__), "assets", "premium_avatar.png")
    avatar_b64 = get_base64_image(avatar_asset)
    
    if avatar_b64:
        img_html = f'<img src="data:image/png;base64,{avatar_b64}" alt="KALI Core">'
    else:
        img_html = '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3N2NncwZ3JtcmN0Ym15bm15bm15bm15bm15bm1/l0HlRnAWXjnBYQV7W/giphy.gif" alt="BEE Core Offline">'

    # Keyword Processing
    message = highlight_keywords(message)
    status_class = f"status-{status}"
    
    # ELITE STRUCTURAL RENDER (Zero Whitespace)
    st.markdown(f"""<div class="avatar-container {status_class}">
<div class="avatar-orb">
{img_html}
</div>
<div class="ai-speech-bubble">
<p style="font-size:0.6rem; color:var(--neon-blue); font-family:'JetBrains Mono'; margin-bottom:10px; opacity:0.6;">
>> KALI_OS::{context.upper()} // STATUS::{status.upper()}
</p>
<div class="typewriter">
<p>{message}</p>
</div>
</div>
<div style="display: flex; justify-content: center; gap: 8px; margin-top: 25px;">
<div class="wave"></div>
<div class="wave"></div>
<div class="wave"></div>
</div>
</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
    render_ai_avatar(context="Evaluation", message="Initializing KALI V4.1 Cognitive Core.", status="idle")
