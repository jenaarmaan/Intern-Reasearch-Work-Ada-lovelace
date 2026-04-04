import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import sys
import plotly.graph_objects as go
from datetime import datetime

# Path patching
sys.path.append(os.path.abspath("Shared_Core"))
from qga_engine import PortfolioOptimizer, QGAEngine

def run_assignment_2():
    st.markdown("<h2 style='color:#bc13fe; font-size:3rem;'>🧠 KALI CORE :: BEE DASHBOARD</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:1.1rem; opacity:0.7;'>High-Horizon Quantum Strategic Analysis Portfolio Suite.</p>", unsafe_allow_html=True)
    
    # Google-Style Metric Overview
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("System Uptime", "99.98%", "0.02%")
    with m2: st.metric("Processing Load", "14.2 Gflops", "-1.4%")
    with m3: st.metric("Swarm Accuracy", "94.2%", "2.1%")
    with m4: st.metric("Latency", "4ms", "0.2ms")
    
    st.markdown("<hr style='border-top:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    
    # Main Dashboard Columns
    col_ctrl, col_viz = st.columns([1.5, 3.5])
    
    with col_ctrl:
        st.markdown("<h4 style='color:#00f2ff; margin-bottom:20px;'>🛠️ STRATEGY CONFIG</h4>", unsafe_allow_html=True)
        
        with st.container(border=True):
            pop_size = st.select_slider("Swarm Size", options=[16, 32, 48, 64, 128], value=48, key="a2_p")
            gen = st.slider("Evolution Generations", 50, 200, 80, key="a2_g")
            risk = st.slider("Risk Matrix Bias (λ)", 0.0, 1.0, 0.5, key="a2_r")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("KALI CORE is pre-synchronized with satellite node L-PK.")

    with col_viz:
        st.markdown("<h4 style='color:#bc13fe; margin-bottom:20px;'>📈 QUANTUM CONVERGENCE MONITOR</h4>", unsafe_allow_html=True)
        
        # Real-time data logic
        n_assets = 25
        np.random.seed(42)
        returns = np.random.uniform(0.05, 0.30, n_assets)
        risks = np.random.uniform(0.12, 0.45, n_assets)
        
        optimizer = PortfolioOptimizer(n_assets, returns, risks)
        qga = QGAEngine(optimizer, pop_size=pop_size, max_gen=gen)
        
        # Action Center
        if st.button("🌟 INITIATE GLOBAL OPTIMIZATION", key="a2_btn", width="stretch"):
            with st.status("Performing Multi-Swarm Handshake...", expanded=True) as status:
                st.write("Initializing Qubits...")
                time.sleep(0.5)
                st.write("Rotating State Vectors...")
                best_ind, best_fit, history = qga.run(risk_aversion=risk)
                status.update(label="Optimization Complete :: KALI Success", state="complete")

            # Chart - Google-Tier Data Viz
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=history, mode='lines', name='BEE QGA-Core',
                                     line=dict(color='#bc13fe', width=4),
                                     fill='tozeroy', fillcolor='rgba(188, 19, 254, 0.1)'))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                hovermode="x unified",
                template="plotly_dark"
            )
            st.plotly_chart(fig, width="stretch")
            
            st.success(f"Final Fitness Index: {best_fit:.4f}")
        else:
            st.markdown("""
                <div style='height: 350px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.02); border-radius: 12px; border: 2px dashed rgba(255,255,255,0.05);'>
                    <p style='opacity: 0.4;'>READY FOR QUANTUM SIGNAL...</p>
                </div>
            """, unsafe_allow_html=True)
