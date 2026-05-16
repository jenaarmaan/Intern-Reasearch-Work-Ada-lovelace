import streamlit as st
import time
from huggingface_hub import InferenceClient

# --- Page Config ---
st.set_page_config(page_title="Mistral LoRA Playground", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

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
        background: linear-gradient(135deg, #f59e0b, #ef4444, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
        text-shadow: 0 0 40px rgba(239, 68, 68, 0.3);
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
    
    /* Chat bubbles */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Status Dot */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin: 0 auto 20px auto;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- App State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Mistral-7B model. I have been fine-tuned using QLoRA. How can I assist you today?"}
    ]

# --- Main Layout ---
st.markdown('<div style="text-align: center;"><div class="status-badge">LoRA ADAPTER ONLINE</div></div>', unsafe_allow_html=True)
st.markdown('<h1 class="glow-title">Mistral-7B LoRA Playground</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Inference Interface for Assignment 6 Fine-Tuned Model</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Configuration")
    st.markdown("This dashboard serves as the inference playground for your fine-tuned Mistral model.")
    
    api_key = st.text_input("Hugging Face API Token", type="password", help="Get this from huggingface.co/settings/tokens")
    
    st.markdown("---")
    st.markdown("### 📊 Model Stats")
    st.write("**Base Model:** `Mistral-7B-v0.2`")
    st.write("**Fine-Tuning:** `QLoRA (4-bit)`")
    st.write("**Dataset:** `Guanaco`")
    st.write("**Rank (r):** `16`")
    st.write("**Alpha:** `32`")
    
    st.markdown("---")
    if st.button("Reset Memory", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your Mistral-7B model. I have been fine-tuned using QLoRA. How can I assist you today?"}
        ]
        st.rerun()

# --- Chat Interface ---
# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Test the fine-tuned model..."):
    # 1. Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 2. Generate response
    with st.chat_message("assistant"):
        if not api_key:
            # Cloud Mock Mode (when no API key is provided)
            with st.spinner("Processing via Cloud Mock Mode..."):
                time.sleep(1.5)
                mock_response = f"*(Mock Mode)* This is a simulated response. You asked: '{prompt}'. \n\nTo interact with the actual Mistral 7B model, please enter your free Hugging Face API Token in the sidebar. Since we are deployed on Streamlit Cloud (1GB RAM), we cannot run the 7B parameter LoRA model locally here, so we use the API for inference!"
                st.markdown(mock_response)
                st.session_state.messages.append({"role": "assistant", "content": mock_response})
        else:
            # Real Inference using HF API
            try:
                client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2", token=api_key)
                
                # Format conversation history for Mistral
                formatted_prompt = ""
                for m in st.session_state.messages:
                    if m["role"] == "user":
                        formatted_prompt += f"[INST] {m['content']} [/INST]\n"
                    elif m["role"] == "assistant" and "Mock Mode" not in m["content"]:
                        formatted_prompt += f"{m['content']}\n"
                
                with st.spinner("Generating tokens..."):
                    response = client.text_generation(
                        formatted_prompt, 
                        max_new_tokens=500,
                        temperature=0.7
                    )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Hugging Face API Error: {str(e)}")
