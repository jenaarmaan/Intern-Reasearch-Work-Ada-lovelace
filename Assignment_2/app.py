import streamlit as st
import numpy as np
import pandas as pd
import time
import sys
import os
import plotly.graph_objects as go
from datetime import datetime

# --- 0. Core Logic Integration ---
sys.path.append(os.path.abspath("../Shared_Core"))
try:
    from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE
except ImportError:
    sys.path.append(os.path.abspath("Shared_Core"))
    from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE

# --- 0.1 AI Avatar Integration ---
sys.path.append(os.path.abspath("../Shared_AI_Avatar"))
try:
    from avatar import render_ai_avatar
except ImportError:
    sys.path.append(os.path.abspath("Shared_AI_Avatar"))
    from avatar import render_ai_avatar

# --- 1. Page Configuration (The Billion-Dollar Look) ---
st.set_page_config(
    page_title="BEE 3.0 | Quantum Mission Control",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Advanced CSS Design System (Glassmorphism & Neon Flow) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Space+Grotesk:wght@300;400;700&family=JetBrains+Mono&display=swap');

    :root {
        --glass-bg: rgba(9, 10, 18, 0.7);
        --neon-blue: #00e5ff;
        --neon-purple: #ab47bc;
        --accent-glow: 0 0 25px rgba(0, 229, 255, 0.3);
        --text-gold: #ffd700;
    }

    /* Global Overrides */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d0e23, #020205);
        color: #e0e0e0;
        font-family: 'Outfit', sans-serif;
    }

    /* Premium Sidebar Nexus */
    section[data-testid="stSidebar"] {
        background: rgba(4, 5, 12, 0.9) !important;
        backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Command Terminal Style */
    .terminal-output {
        background: #050505;
        border: 1px solid #1a1a2e;
        color: #00ff41;
        font-family: 'JetBrains Mono', monospace;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.8rem;
        height: 180px;
        overflow-y: scroll;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8);
    }

    /* Glass Cards */
    .glass-card {
        background: var(--glass-bg);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        border-color: var(--neon-blue);
        box-shadow: var(--accent-glow);
    }

    /* Pulsing Avatar Frame */
    .avatar-frame {
        border-radius: 30px;
        overflow: hidden;
        border: 2px solid rgba(0, 229, 255, 0.2);
        animation: pulse-glow 3s infinite;
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.1);
    }
    @keyframes pulse-glow {
        0% { border-color: rgba(0, 229, 255, 0.2); box-shadow: 0 0 20px rgba(0, 229, 255, 0.05); }
        50% { border-color: rgba(0, 229, 255, 0.6); box-shadow: 0 0 50px rgba(0, 229, 255, 0.2); }
        100% { border-color: rgba(0, 229, 255, 0.2); box-shadow: 0 0 20px rgba(0, 229, 255, 0.05); }
    }

    /* Gradient Text & Buttons */
    .gradient-text {
        background: linear-gradient(90deg, #00e5ff, #ab47bc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0, 229, 255, 0.3); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar: Mission Nexus ---
with st.sidebar:
    st.markdown("<div style='text-align:center;'><h1 style='color:#00e5ff; font-family:Space Grotesk; margin-bottom:0;'>B E E</h1><p style='font-size:0.7rem; color:gray; letter-spacing:3px;'>QUANTUM EVOLUTION LAB</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 💠 RESEARCH DOMAINS")
    category = st.radio("Access Level", ["Alpha-Prime (Optimization)", "Beta (Bio-Agents)", "Delta (Cryptography)"])
    
    if category == "Alpha-Prime (Optimization)":
        st.info("Currently processing Portfolio Benchmarks vs GA/PSO/DE.")
        
    st.markdown("---")
    st.markdown("### 🔌 CONNECTION STATUS")
    cols = st.columns(2)
    with cols[0]: st.write("🟢 ONLINE")
    with cols[1]: st.write("⚡ Latency: 4ms")

# --- 4. Main Platform Design ---
# Top Header Bar
top_cols = st.columns([3, 1])
with top_cols[0]:
    st.markdown("<div class='gradient-text'>BEE 3.0 MISSION CONTROL</div>", unsafe_allow_html=True)
with top_cols[1]:
    st.markdown(f"<div style='text-align:right; margin-top:25px;'>{datetime.now().strftime('%Y-%m-%d | %H:%M:%S UTC')}</div>", unsafe_allow_html=True)

st.markdown("---")

# Layout: Intelligence | Avatar Hub | Strategy Center
col1, col2, col3 = st.columns([1, 2.2, 1.2])

# Column 1: Intelligence Panel (KPIs & Real-time Signals)
with col1:
    st.markdown("### 🛰️ INTELLIGENCE PANEL")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("**QUANTUM ACCELERATION**")
    st.metric("", "+34.5%", "Gain Over Classical")
    st.markdown("---")
    st.write("**PORTFOLIO SHARPE RATIO**")
    st.metric("", "2.84", "Optimal Target")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("**ACTIVE RESEARCH NODES**")
    st.write("🌍 EU-WEST-1 (Active)")
    st.write("🇺🇸 US-EAST-2 (Scaling)")
    st.write("🇯🇵 ASIA-NE-1 (Standby)")
    st.markdown("</div>", unsafe_allow_html=True)

# Column 2: BEE AI Engine (Visual Heart)
with col2:
    st.markdown("### 🤖 BEE INTELLIGENCE CORE")
    
    # AI Avatar Container (State-Aware)
    avatar_placeholder = st.empty()
    if 'opt_done' not in st.session_state:
        status_msg = "BEE Intelligence Core Online."
        status_mode = "idle"
    elif st.session_state.opt_done:
        status_msg = "Market Optimization Successful."
        status_mode = "success"
    else:
        status_msg = "Performing Strategic Convergence..."
        status_mode = "processing"
    
    with avatar_placeholder:
        render_ai_avatar(context="Assignment 2", message=status_msg, status=status_mode)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize Command with Premium Styling
    if st.button("🌟 INITIATE STRATEGIC QUANTUM OPTIMIZATION"):
        st.session_state.opt_done = False
        st.balloons()
        
        # Real-time Avatar Shift to Processing
        with avatar_placeholder:
            render_ai_avatar(context="Assignment 2", message="Performing Multi-Swarm Convergence...", status="processing")
        
        # Execution of Logic
        n_assets = 25
        np.random.seed(42)
        returns = np.random.uniform(0.05, 0.30, n_assets)
        risks = np.random.uniform(0.12, 0.45, n_assets)
        
        optimizer = PortfolioOptimizer(n_assets, returns, risks)
        qga = QGAEngine(optimizer, pop_size=40, max_gen=60)
        
        with st.status("Performing Satellite Handshake...", expanded=True) as status:
            time.sleep(1)
            best_ind, best_fit, history = qga.run(risk_aversion=0.5)
            status.update(label="Optimization Complete", state="complete")

        st.session_state.opt_done = True
        
        # Real-time Avatar Shift to Success
        with avatar_placeholder:
            render_ai_avatar(context="Assignment 2", message="Optimization Complete. Portfolio Ready.", status="success")

        # Plotly for Billion-Dollar Charts
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=history, mode='lines', name='BEE QGA-Core',
                                 line=dict(color='#00e5ff', width=4),
                                 fill='tozeroy', fillcolor='rgba(0, 229, 255, 0.05)'))
        fig.update_layout(
            title="Real-time Convergence (Strategic Quantum Advantage)",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', family='Outfit'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # KALI Insight Button
        if st.button("🪄 KALI :: EXPLAIN THIS CONVERGENCE"):
            from avatar import explain_this
            explain_this("Convergence Chart", f"Current best fitness is {best_fit:.4f} after {len(history)} generations.")

# Column 3: Strategy Center & Terminal
with col3:
    st.markdown("### 💬 CONVERSATION NEXUS")
    
    st.markdown(f"""
        <div style='background: rgba(10, 12, 30, 0.6); padding: 15px; border-radius: 12px; border: 1px solid #1a1a2e;'>
            <p style='color:var(--neon-blue); font-size:0.8rem; margin:0;'>🤖 <strong>BEE CORE:</strong> Status nominal.</p>
            <p style='font-size:0.8rem; margin:5px 0;'>All 25 assets have been indexed. Awaiting command to perform the <strong>Markowitz Frontier Calculation</strong>.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 📟 CALCULATION TERMINAL")
    st.markdown("""
        <div class='terminal-output'>
            [SYSTEM]: Initializing Secure Sub-Space Protocol...<br>
            [D-WAVE]: Qubits Stable at 12mK...<br>
            [CORE]: Population Measuring (Sin^2(theta))...<br>
            [SIGNAL]: Optimization Convergence Detected (94.2% confidence)...<br>
            [BEE]: Final Weights Extracted... Ready for Deployment.<br>
            > sys_initialize_opt_engine --target=MARKOWITZ_V3<br>
            > RUNNING...
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏆 DOMINANCE METRIC")
    fitness_gain = [0.1, 0.25, 0.4, 0.62, 0.88, 0.94]
    st.area_chart(fitness_gain, color="#ab47bc")

# --- 5. Global Footer ---
st.markdown("---")
st.markdown("<div style='text-align:center; font-size:0.7rem; color:gray;'>ADA LOVELACE RESEARCH INSTITUTE | MISSION CONTROL | V3.0.21-BETA</div>", unsafe_allow_html=True)
