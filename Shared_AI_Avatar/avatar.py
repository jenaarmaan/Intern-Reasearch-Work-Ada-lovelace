import streamlit as st
import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render_ai_avatar(context="General Research", message="Status nominal.", status="idle"):
    """
    World-Class AI Avatar Renderer - V2.0
    Args:
        context (str): Research domain or assignment name.
        message (str): Speech bubble text.
        status (str): 'idle', 'processing', or 'success'.
    """
    
    # Load Elite Design System
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Path to high-res avatar asset
    avatar_asset = os.path.join(os.path.dirname(__file__), "assets", "premium_avatar.png")
    
    if os.path.exists(avatar_asset):
        avatar_b64 = get_base64_image(avatar_asset)
        img_html = f'<img src="data:image/png;base64,{avatar_b64}" alt="AI Avatar Core">'
    else:
        img_html = '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3N2NncwZ3JtcmN0Ym15bm15bm15bm15bm15bm15bm1/l0HlRnAWXjnBYQV7W/giphy.gif" alt="BEE Core Offline">'

    # Dynamic Class Mapping
    status_class = f"status-{status}"
    
    # Render Structural HTML
    st.markdown(f"""
        <div class="avatar-container {status_class}">
            <div class="avatar-orb">
                {img_html}
            </div>
            
            <div class="ai-speech-bubble">
                <p style="font-size:0.6rem; color:var(--neon-blue); font-family:'JetBrains Mono'; margin-bottom:10px; opacity:0.6;">
                    >> DOMAIN::{context.upper()} // STATUS::{status.upper()}
                </p>
                <div class="typewriter">
                    <p style="margin:0; font-family:'Outfit'; color:#e0e0e0; font-size:1.1rem;">{message}</p>
                </div>
            </div>
            
            <div class="thought-waves" style="display: flex; justify-content: center; gap: 8px; margin-top: 20px;">
                <div class="wave" style="width: 3px; height: 15px; background: var(--neon-blue); opacity: 0.3; border-radius: 4px;"></div>
                <div class="wave" style="width: 3px; height: 15px; background: var(--neon-blue); opacity: 0.3; border-radius: 4px;"></div>
                <div class="wave" style="width: 3px; height: 15px; background: var(--neon-blue); opacity: 0.3; border-radius: 4px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
    render_ai_avatar(context="Evaluation Lab", message="Core System V2.0 Online.", status="idle")
