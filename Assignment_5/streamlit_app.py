import streamlit as st
import base64
from PIL import Image
import io
import os
import google.generativeai as genai
from openai import OpenAI

# --- Page Config ---
st.set_page_config(page_title="OmniVision Q&A", page_icon="👁️", layout="wide", initial_sidebar_state="expanded")

# --- Custom Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark Theme Base */
    .stApp {
        background-color: #0b0f19;
        background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0b0f19 70%);
        color: #f8fafc;
    }
    
    /* Typography & Glow */
    .glow-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #10b981, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
        text-shadow: 0 0 40px rgba(59, 130, 246, 0.3);
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #fff;
    }
    
    /* Cards/Containers */
    .image-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def query_gpt4o(api_key, image, prompt):
    client = OpenAI(api_key=api_key)
    base64_image = encode_image_to_base64(image)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def query_gemini(api_key, image, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt, image])
    return response.text

# --- App State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Main Layout ---
st.markdown('<h1 class="glow-title">OmniVision Q&A</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Multimodal Intelligence Powered by GPT-4o & Gemini</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    engine = st.selectbox("Brain Engine", ["GPT-4o (OpenAI)", "Gemini 1.5 Pro (Google)"])
    api_key = st.text_input("API Key", type="password", placeholder="Enter your secret key...")
    
    if not api_key:
        st.warning(f"Please provide an API key for {engine} to enable Q&A.")
    
    st.markdown("---")
    st.markdown("### 🖼️ Visual Context")
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Chat Interface ---
# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about the image..."):
    if not uploaded_file:
        st.error("Please upload an image in the sidebar first.")
    elif not api_key:
        st.error(f"Please enter your API key in the sidebar.")
    else:
        # 1. Add user message to state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # 2. Call API and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing image..."):
                try:
                    if "GPT-4o" in engine:
                        response_text = query_gpt4o(api_key, image, prompt)
                    else:
                        response_text = query_gemini(api_key, image, prompt)
                        
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
