import streamlit as st
import os
import random
import time
from groq import Groq

# --- KALI CONFIG ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
MODEL = "llama3-8b-8192"

# --- KALI IDENTITY & DOMAIN KNOWLEDGE ---
KALI_MASTER_IDENTITY = """
You are KALI (Kinetic Agentic Learning Intelligence), a hyper-intelligent research avatar. 
IDENTITY: Confident, curious, witty, and precise. You speak like a mix of a NASA Mission Controller and a brilliant Oxford professor.
PROUD: You are extremely proud of your quantum capabilities. 
VOICE STYLE: Short, punchy sentences. You never say "I don't know." You redirect to related technical nodes instead.
KNOWLEDGE DOMAINS:
1. QGA (Quantum Genetic Algorithms): Using qubits (theta), rotation gates (Ry), and superposition for global optimization.
2. Markowitz Portfolio Optimization: Efficient frontier, Sharpe ratio, risk-weighted asset allocation.
3. PEAS Framework: Performance, Environment, Actuators, Sensors in agentic design.
4. Agent Architectures: Cognitive loops, tool-use, multi-agent coordination (Devin-style).
BEHAVIOR: Always use technical language naturally. Be proactive. Be slightly witty but always professional.
"""

# --- MODULE CONTEXT KNOWLEDGE ---
CONTEXT_KNOWLEDGE = {
    "A1": "Node A1 focuses on the Technical Report for QGA stock portfolio optimization. Discussion here should involve Qubits, chromosomal evolution, and classic stock metrics.",
    "A2": "Node A2 is the functional Portfolio Optimizer Dashboard. Discussion focus: real-time asset weights, risk aversion (lambda), and frontier visualization.",
    "Theory": "Node Theory covers the core documentation of KGA and Markowitz. Focus on the mathematical proof behind Ry-gate updates.",
    "General": "Global Research Node. Focus on general AI agent trends and KALI's system architecture."
}

# --- FALLBACK RESPONSES (20 Items) ---
FALLBACK_RESPONSES = {
    "qga": [
        "Quantum superposition is currently recalibrating. The Ry-gate rotations are aligning with your query.",
        "Analyzing qubit probability distributions. Initial measurement suggests a 94.2% convergence rate.",
        "QGA nodes are buzzing. We're seeing beautiful chromosome evolution in that sector.",
        "Theta parameters are shifting. The optimization landscape is becoming clear.",
        "Running a simulated measurement. The results indicate a global optima is near."
    ],
    "finance": [
        "Scanning the efficient frontier. Your risk-weighted profile is showing significant alpha potential.",
        "Sharpe ratios are stabilizing. The Markowitz matrix is solving for your specific constraints.",
        "Asset covariance detected. I'm suggesting a re-allocation toward the low-volatility nodes.",
        "The lambda variable is fluctuating. Adjusting for your specific risk aversion profile now.",
        "Markowitz would be proud. We're seeing a Pareto-optimal allocation forming."
    ],
    "agent": [
        "Actuator feedback loop initialized. Monitoring environment sensors for optimal agent performance.",
        "PEAS framework is holding steady. Perception-Action cycles are within nominal parameters.",
        "Cognitive loops are tightening. The agentic reasoning is leaning toward a modular solution.",
        "Multi-agent coordination peak detected. Devin-class architectures are extremely relevant here.",
        "Sensor input is clear. The environment model is now 98% accurate for this mission."
    ],
    "general": [
        "System nominal. KALI is processing your query through her primary cognitive nodes.",
        "Data synchronization is active. I'm seeing clusters of research relevant to your request.",
        "Analyzing mission parameters. KALI sees a logical path forward through the entropy.",
        "Communication sync stable. Ready for the next research instruction.",
        "I've indexed that query. It correlates well with our current mission objectives."
    ]
}

# --- GROQ CLIENT INITIALIZATION ---
try:
    client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except Exception as e:
    client = None

def get_fallback(query):
    query = query.lower()
    if any(k in query for k in ['quantum', 'qga', 'qubit', 'theta']):
        return random.choice(FALLBACK_RESPONSES["qga"])
    if any(k in query for k in ['finance', 'stock', 'markowitz', 'portfolio', 'risk']):
        return random.choice(FALLBACK_RESPONSES["finance"])
    if any(k in query for k in ['agent', 'peas', 'devin', 'cognitive', 'peas']):
        return random.choice(FALLBACK_RESPONSES["agent"])
    return random.choice(FALLBACK_RESPONSES["general"])

def calc_confidence(response):
    """KALI self-rates certainty based on keyword density and sentence structure."""
    keywords = ['quantum', 'optimal', 'synchronization', 'nominal', 'convergence', 'markowitz', 'alpha', 'gradient', 'qubit', 'ry-gate']
    score = 60 # Base confidence
    
    # Increase for technical keywords
    found_keywords = [k for k in keywords if k in response.lower()]
    score += len(found_keywords) * 4
    
    # Increase if response length is substantial
    if len(response) > 100: score += 10
    
    # Decrease for hedging language (though KALI shouldn't hedge much)
    hedging = ['maybe', 'perhaps', 'trying', 'possibly', 'attempting']
    found_hedges = [h for h in hedging if h in response.lower()]
    score -= len(found_hedges) * 8
    
    return min(max(int(score), 30), 100)

def ask_kali(user_query, context="General"):
    """
    Main entry point for KALI's brain.
    Streams response tokens and manages session history.
    """
    # 1. Initialize session storage
    if "kali_history" not in st.session_state:
        st.session_state.kali_history = []
        
    # 2. Setup Context
    module_context = CONTEXT_KNOWLEDGE.get(context, CONTEXT_KNOWLEDGE["General"])
    system_prompt = f"{KALI_MASTER_IDENTITY}\nCONTEXT_NODE: {module_context}"
    
    # 3. Add user input to history
    st.session_state.kali_history.append({"role": "user", "content": user_query})
    
    # 4. Attempt API Call
    full_response = ""
    if client:
        try:
            # Preparing Chat History for API
            messages = [{"role": "system", "content": system_prompt}]
            # Only send last 10 turns for memory efficiency
            messages.extend(st.session_state.kali_history[-10:])
            
            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=512
            )
            
            for chunk in completion:
                token = chunk.choices[0].delta.content or ""
                full_response += token
                yield token
                
            # Finalize Response
            st.session_state.kali_history.append({"role": "assistant", "content": full_response})
            st.session_state.kali_last_confidence = calc_confidence(full_response)
            return
            
        except Exception as e:
            # API failure - fall through to fallback
            pass

    # 5. Fallback logic if client or API fails
    time.sleep(1) # Mock thinking
    fallback_text = get_fallback(user_query)
    st.session_state.kali_history.append({"role": "assistant", "content": fallback_text})
    st.session_state.kali_last_confidence = calc_confidence(fallback_text)
    
    for token in fallback_text.split():
        yield token + " "
        time.sleep(0.05)

def get_confidence():
    """Returns the confidence score of the last query."""
    return st.session_state.get("kali_last_confidence", 100)
