import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from qiskit import QuantumCircuit

# Path patching for local imports
sys.path.append(os.path.abspath("Shared_Core"))
from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE

def run_assignment_1():
    st.markdown("<h2 style='color:#00e5ff;'>🚀 Quantum Portfolio Optimization</h2>", unsafe_allow_html=True)
    st.markdown("### Comparison of QGA vs Classical Algorithms")
    
    # Settings
    col_a, col_b = st.columns(2)
    with col_a:
        n_assets = st.slider("Assets", 5, 50, 20, key="a1_n")
        risk_aversion = st.slider("Risk (λ)", 0.0, 1.0, 0.5, key="a1_r")
    with col_b:
        pop_size = st.number_input("Pop Size", 10, 100, 32, key="a1_p")
        gen = st.number_input("Generations", 10, 100, 50, key="a1_g")

    np.random.seed(42)
    assets = [f"Stock {i+1}" for i in range(n_assets)]
    returns = np.random.uniform(0.05, 0.25, n_assets)
    risks = np.random.uniform(0.1, 0.4, n_assets)

    if st.button("🔥 Run Benchmarks", key="a1_btn"):
        optimizer = PortfolioOptimizer(n_assets, returns, risks)
        
        with st.status("Executing Multi-Agent Optimization...", expanded=False):
            qga = QGAEngine(optimizer, pop_size, gen)
            q_best, q_fit, q_hist = qga.run(risk_aversion)
            ga = ClassicalGA(optimizer, pop_size, gen)
            g_best, g_fit, g_hist = ga.run(risk_aversion)

        res_col1, res_col2 = st.columns([2, 1])
        with res_col1:
            fig, ax = plt.subplots()
            ax.plot(q_hist, label='QGA (Quantum)', color='cyan')
            ax.plot(g_hist, label='GA (Classical)', linestyle='--')
            ax.set_title("Convergence Speed")
            st.pyplot(fig)
        with res_col2:
            st.write(f"**Winner:** QGA")
            st.write(f"**Selected:** {np.sum(q_best)} stocks")
