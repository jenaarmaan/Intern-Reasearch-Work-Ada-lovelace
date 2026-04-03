import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import sys
import plotly.graph_objects as go
from datetime import datetime

# Path patching for local imports
sys.path.append(os.path.abspath("Shared_Core"))
from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE

def run_assignment_2():
    st.markdown("<h1 style='color:#ab47bc;'>💠 BEE DASHBOARD V3.0</h1>", unsafe_allow_html=True)
    st.markdown("### Quantum Mission Control - (Assignment 2 Integration)")
    
    # Layout Optimization
    col1, col2 = st.columns([1.5, 3.5])
    
    with col1:
        st.markdown("<h4 style='color:var(--neon-blue);'>🧬 GENETIC PARAMETERS</h4>", unsafe_allow_html=True)
        pop_size = st.slider("Swarm Population", 20, 100, 48, key="a2_p")
        gen = st.slider("Total Generations", 50, 200, 64, key="a2_g")
        risk = st.slider("Risk Matrix (λ)", 0.0, 1.0, 0.5, key="a2_r")
        st.markdown("---")
        st.write("**LATENCY:** 4ms")

    with col2:
        st.markdown("<h4 style='color:var(--neon-blue);'>🛰️ CONVERGENCE MONITOR</h4>", unsafe_allow_html=True)
        
        # Real-time data generation logic for BEE
        n_assets = 25
        np.random.seed(42)
        returns = np.random.uniform(0.05, 0.30, n_assets)
        risks = np.random.uniform(0.12, 0.45, n_assets)
        
        optimizer = PortfolioOptimizer(n_assets, returns, risks)
        qga = QGAEngine(optimizer, pop_size=pop_size, max_gen=gen)
        
        if st.button("🌟 START GLOBAL OPTIMIZATION", key="a2_btn"):
            with st.status("Performing Multi-Swarm Handshake...", expanded=True) as status:
                best_ind, best_fit, history = qga.run(risk_aversion=risk)
                status.update(label="Complete", state="complete")

            # Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=history, mode='lines', name='BEE QGA-Core',
                                     line=dict(color='#ab47bc', width=3),
                                     fill='tozeroy', fillcolor='rgba(171, 71, 188, 0.1)'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
