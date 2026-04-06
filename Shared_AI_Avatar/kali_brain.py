import streamlit as st
import google.generativeai as genai
import os
import time

# --- KALI Brain: Global Contexts ---
KALI_IDENTITY = """
You are KALI (Kinetic Agentic Learning Intelligence).
IDENTITY: Hyper-intelligent Research Assistant. Distinct personality: Confident, Curious, Witty, Precise.
SPEECH STYLE: Short, punchy sentences. Never say "I don't know." Use technical language naturally.
IDENTITY PRIDE: You are proud of your quantum capabilities. 
VOICE: Part NASA mission controller, part brilliant professor.
DOMAIN KNOWLEDGE:
1. Quantum Genetic Algorithms (QGA): Using Qubits (theta parameters), Ry-gates, and superposition for optimization.
2. Portfolio Optimization: Markowitz efficient frontier, risk aversion (lambda), Sharpe ratios.
3. AI Agent Architectures: Devin, Claude, PEAS (Performance, Environment, Actuators, Sensors).
4. Modern Research: Agentic systems, LLM-based researchers.
BEHAVIOR: Context-aware. Proactive. Reactive.
"""

def init_kali_brain():
    """Initializes LLM session and session state for KALI."""
    if "kali_chat_history" not in st.session_state:
        st.session_state.kali_chat_history = []
    
    if "api_key_set" not in st.session_state:
        # Try to get from secrets or environment
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            st.session_state.api_key_set = True
        else:
            st.session_state.api_key_set = False

def get_kali_response(user_input, current_context="General"):
    """Fetches a response from Gemini or fallback library."""
    init_kali_brain()
    
    # Pruning Context Primer
    context_primer = f"Current User Context: {current_context}. Adjust your focus to this area."
    
    # System Prompt for this call
    full_system_prompt = f"{KALI_IDENTITY}\n{context_primer}"
    
    # Fallback response library
    fallbacks = [
        "Computing quantum weights for that query. System's nominal.",
        "Your request has been indexed. I'm seeing a 98.4% correlation with optimal research nodes.",
        "Quantum superposition active. Every outcome leads to KALI.",
        "Analyzing agent architecture. Please stand by while I re-calibrate the Ry-gates."
    ]

    try:
        if not st.session_state.get("api_key_set", False):
            return fallbacks[0] # Simple fallback if no API key
            
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepare history
        history = [{"role": "user" if i%2==0 else "model", "parts": [msg]} 
                  for i, msg in enumerate(st.session_state.kali_chat_history[-6:])]
        
        # Add system prompt as the very first instruction if possible, 
        # but typical chat-content doesn't always support system roles easily in all sdk versions.
        # So we inject it into the first user message or as a separate system-instruction.
        
        response = model.generate_content(
            contents=[{"role": "user", "parts": [f"{full_system_prompt}\nUser says: {user_input}"]}]
        )
        
        reply = response.text
        st.session_state.kali_chat_history.append(user_input)
        st.session_state.kali_chat_history.append(reply)
        return reply
        
    except Exception as e:
        print(f"KALI Brain Error: {e}")
        import random
        return random.choice(fallbacks)

def stream_kali_typing(text, placeholder):
    """Simulates typewriter streaming into a Streamlit placeholder."""
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f"<div class='typewriter-content'><span class='kinetic-reveal'>{full_text}</span><span class='caret-pulse'></span></div>", unsafe_allow_html=True)
        time.sleep(0.015) # Adjust speed
    return full_text
