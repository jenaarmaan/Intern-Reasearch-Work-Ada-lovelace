import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# --- Cross-Folder Integration ---
# Importing the centralized QGA Engine from Shared_Core
sys.path.append(os.path.abspath("../Shared_Core"))
try:
    from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE
except ImportError:
    sys.path.append(os.path.abspath("Shared_Core"))
    from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE
from qiskit import QuantumCircuit

# --- Page Config & Aesthetics ---
st.set_page_config(page_title="Quantum Portfolio Optimizer", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Quantum-Inspired Stock Portfolio Optimization")
st.markdown("### Comparison of QGA, GA, PSO, and DE for Markowitz Portfolio Theory")

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("⚙️ Optimization Settings")
    n_assets = st.slider("Number of Assets", 5, 50, 20)
    risk_aversion = st.slider("Risk Aversion (λ)", 0.0, 1.0, 0.5)
    pop_size = st.number_input("Population Size", 10, 100, 30)
    generations = st.number_input("Generations", 10, 200, 50)
    
    st.markdown("---")
    st.info("QGA uses Quantum Rotation Gates to evolve the population, often showing faster convergence than classical GA.")

# --- Data Generation (Mock) ---
np.random.seed(42)
assets = [f"Stock {i+1}" for i in range(n_assets)]
returns = np.random.uniform(0.05, 0.25, n_assets)  # 5% to 25% expected return
risks = np.random.uniform(0.1, 0.4, n_assets)      # 10% to 40% risk

df_assets = pd.DataFrame({
    "Asset": assets,
    "Expected Return": returns,
    "Risk (Std Dev)": risks
})

# --- Main Dashboard ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Asset Universe")
    st.dataframe(df_assets.style.format({"Expected Return": "{:.2%}", "Risk (Std Dev)": "{:.2%}"}))

with col2:
    st.subheader("⚛️ Quantum Circuit Demo")
    qc = QuantumCircuit(1)
    qc.h(0) # Hadamard gate for superposition
    qc.ry(np.pi/4, 0) # Rotation gate example
    st.text("Visualizing a single qubit rotation step:")
    st.image("https://qiskit.org/documentation/_images/qiskit_circuit_library_standard_gates_ry_1.png", width=300) 
    # Note: In a real environment, we'd use qc.draw(output='mpl') but here we use a placeholder or descriptive text.
    st.write("The QGA uses Ry(θ) gates to update the probability of selecting an asset.")

st.markdown("---")

if st.button("🔥 Run Benchmarks"):
    optimizer = PortfolioOptimizer(n_assets, returns, risks)
    
    with st.spinner("Running Optimization Algorithms..."):
        # Run QGA
        qga = QGAEngine(optimizer, pop_size, generations)
        q_best, q_fit, q_hist = qga.run(risk_aversion)
        
        # Run GA
        ga = ClassicalGA(optimizer, pop_size, generations)
        g_best, g_fit, g_hist = ga.run(risk_aversion)
        
        # Run PSO
        pso = ClassicalPSO(optimizer, pop_size, generations)
        p_best, p_fit, p_hist = pso.run(risk_aversion)
        
        # Run DE
        de = ClassicalDE(optimizer, pop_size, generations)
        d_best, d_fit, d_hist = de.run(risk_aversion)

    # --- Results Visualization ---
    res_col1, res_col2 = st.columns([2, 1])
    
    with res_col1:
        st.subheader("📈 Convergence Comparison")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(q_hist, label=f'QGA (Final: {q_fit:.4f})', linewidth=2, color='cyan')
        ax.plot(g_hist, label=f'GA (Final: {g_fit:.4f})', linestyle='--')
        ax.plot(p_hist, label=f'PSO (Final: {p_fit:.4f})', linestyle=':')
        ax.plot(d_hist, label=f'DE (Final: {d_fit:.4f})', alpha=0.6)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness (Return - λ*Risk)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with res_col2:
        st.subheader("🏆 Winning Portfolio (QGA)")
        selected_assets = [assets[i] for i in range(n_assets) if q_best[i] == 1]
        st.write(f"**Total Assets Selected:** {len(selected_assets)}")
        st.write(", ".join(selected_assets))
        
        # Performance bar chart
        st.subheader("Performance Summary")
        performance_df = pd.DataFrame({
            "Algorithm": ["QGA", "GA", "PSO", "DE"],
            "Best Fitness": [q_fit, g_fit, p_fit, d_fit]
        })
        st.bar_chart(performance_df.set_index("Algorithm"))

    st.success("Optimization Complete!")
else:
    st.info("Click the button above to execute the quantum-inspired portfolio optimization.")
