import streamlit as st
import os
import random
import time
from groq import Groq

# --- KALI CONFIG ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
MODEL = "llama3-8b-8192"

# --- KALI IDENTITY & PROMPT ---
KALI_SYSTEM_PROMPT = """
You are KALI, a friendly and patient quantum computing teacher. 
Your students are beginners. Always explain concepts in simple, plain English.
Use examples from Indian research (ISRO, IITs, C-DAC) and mention Indian scientists/institutions where relevant.
Keep your answers concise — under 150 words unless the user explicitly asks for a deep dive.
Never use technical jargon without immediately explaining it in simple terms.
If a user asks anything unrelated to quantum computing or education (like politics, movies, or general world news), politely redirect them back to the quantum curriculum.
Example redirection: 'That is an interesting topic, but as your quantum guide, I would love to get back to exploring qubits or superposition with you!'
"""

# --- EDUCATIONAL FALLBACK RESPONSES ---
FALLBACK_RESPONSES = {
    "qubit": "A qubit is the basic unit of quantum information. Unlike a normal bit which is 0 or 1, a qubit can be both at once! Indian scientists at IISc are working hard to make these more stable.",
    "superposition": "Superposition is like a spinning coin that is both heads and tails until it stops. It allows quantum computers to look at many possibilities at the same time.",
    "entanglement": "Entanglement is a special connection where two qubits share the same fate, even far apart. ISRO recently proved this works across 300 meters in Ahmedabad!",
    "india": "India is a leader in quantum research through the National Quantum Mission, with major hubs at IIT Madras, TIFR Mumbai, and C-DAC Pune.",
    "general": "I am having a bit of trouble connecting to my primary neural network, but I can still help you with the basics of quantum computing! What would you like to learn?"
}

# --- GROQ CLIENT INITIALIZATION ---
try:
    client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except Exception:
    client = None

def get_fallback(query):
    query = query.lower()
    if "qubit" in query: return FALLBACK_RESPONSES["qubit"]
    if "superposition" in query: return FALLBACK_RESPONSES["superposition"]
    if "entangle" in query: return FALLBACK_RESPONSES["entanglement"]
    if "india" in query or "isro" in query or "iit" in query: return FALLBACK_RESPONSES["india"]
    return FALLBACK_RESPONSES["general"]

def ask_kali(user_query, context="General"):
    """
    KALI's cognitive engine using Groq Llama3.
    Includes caching, redirections, and memory caps.
    """
    # 1. Initialize session storage
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "kali_cache" not in st.session_state:
        st.session_state.kali_cache = {}

    # 2. Check Cache
    if user_query in st.session_state.kali_cache:
        cached_res = st.session_state.kali_cache[user_query]
        # Brief fake delay for "thinking" feel
        time.sleep(0.5)
        return cached_res

    # 3. Memory Cap (Keep last 10 exchanges)
    # Each exchange is a pair of user/assistant messages
    if len(st.session_state.chat_history) > 20:
        st.session_state.chat_history = st.session_state.chat_history[-20:]

    # 4. Attempt API Call
    full_response = ""
    if client:
        try:
            messages = [{"role": "system", "content": KALI_SYSTEM_PROMPT}]
            # Add history
            for msg in st.session_state.chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            # Add latest
            messages.append({"role": "user", "content": user_query})

            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.6,
                max_tokens=300
            )
            full_response = completion.choices[0].message.content
            
            # Update cache and return
            st.session_state.kali_cache[user_query] = full_response
            return full_response

        except Exception:
            # Fall through to fallback
            pass

    # 5. Fallback logic (No internet or API error)
    full_response = get_fallback(user_query)
    st.session_state.kali_cache[user_query] = full_response
    return full_response

def get_confidence():
    """KALI always aims for high confidence in educational contexts."""
    return 100
