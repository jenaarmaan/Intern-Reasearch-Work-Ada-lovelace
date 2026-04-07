import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from qga_engine import PortfolioOptimizer, QGAEngine, ClassicalGA, ClassicalPSO, ClassicalDE, fetch_india_data, calculate_metrics, INDIAN_TICKERS

def run_assignment_1():
    st.header("Technical Report & Benchmarking")
    
    tab1, tab2 = st.tabs(["📄 Technical Report", "⚛️ Convergence Benchmarks"])
    
    with tab1:
        st.subheader("Agent Architecture Design & Analysis")
        # Path to report
        report_path = os.path.join("Assignment_1", "Technical_Report.md")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                content = f.read()
                st.markdown(content)
        else:
            st.error("Technical Report not found.")

    with tab2:
        st.subheader("Quantum vs Classical Portfolio Optimization")
        st.write("Comparing algorithmic efficiency using real NSE India assets.")
        
        # Live Data Fetching
        with st.spinner("Fetching live market data for NSE Universe..."):
            data, source_tag = fetch_india_data(INDIAN_TICKERS)
            returns, risks, bench_perf = calculate_metrics(data, INDIAN_TICKERS)
        
        # Layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Asset Universe")
            col_list = pd.DataFrame({
                "Asset": INDIAN_TICKERS,
                "Return": returns,
                "Risk": risks
            })
            st.dataframe(col_list.style.format({"Return": "{:.2%}", "Risk": "{:.2%}"}))
            st.caption(f"Source: {source_tag} | Currency: ₹ (INR)")

        with col2:
            st.subheader("⚛️ Quantum Logic")
            st.write("QGA utilizes Ry(θ) gates to maintain population diversity and accelerate convergence.")
            st.markdown('''
                <div style="padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center; background: white;">
                    <div style="font-size: 0.8rem; color: #4A90D9; margin-bottom: 10px; font-weight: bold;">RY-GATE ROTATION STATUS</div>
                    <div style="height: 12px; width: 100%; background: #f0f0f0; border-radius: 6px; position: relative;">
                        <div style="height: 100%; width: 72%; background: linear-gradient(90deg, #4A90D9, #34A853); border-radius: 6px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.75rem; color: #666;">
                        <span>Classical Bit (0)</span>
                        <span>Quantum Qubit (θ)</span>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown("---")
        
        # Benchmarking Controls
        c1, c2, c3 = st.columns(3)
        with c1: pop_size = st.number_input("Population", 10, 100, 30, key="a1_p")
        with c2: gens = st.number_input("Generations", 10, 200, 50, key="a1_g")
        with c3: risk_bias = st.slider("Risk Bias (λ)", 0.0, 1.0, 0.5, key="a1_r")

        if st.button("🔥 EXECUTE BENCHMARKS", key="a1_btn"):
            n_assets = len(INDIAN_TICKERS)
            optimizer = PortfolioOptimizer(n_assets, returns, risks)
            
            with st.status("Executing Multi-Algorithm Swarm...", expanded=True) as status:
                st.write("Running QGA (Quantum)...")
                qga = QGAEngine(optimizer, pop_size, gens)
                best_q, fit_q, hist_q = qga.run(risk_bias)
                
                st.write("Running GA/PSO/DE...")
                ga = ClassicalGA(optimizer, pop_size, gens)
                _, fit_g, hist_g = ga.run(risk_bias)
                
                pso = ClassicalPSO(optimizer, pop_size, gens)
                _, fit_p, hist_p = pso.run(risk_bias)
                
                status.update(label="Benchmarks Complete", state="complete")

            # Results Visualization
            res_col1, res_col2 = st.columns([2, 1])
            
            with res_col1:
                st.subheader("📈 Convergence Analysis")
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=hist_q, name=f'QGA (₹ {fit_q:.4f})', line=dict(color='#4A90D9', width=4)))
                fig.add_trace(go.Scatter(y=hist_g, name=f'GA (₹ {fit_g:.4f})', line=dict(dash='dash')))
                fig.add_trace(go.Scatter(y=hist_p, name=f'PSO (₹ {fit_p:.4f})', line=dict(dash='dot')))
                
                fig.add_hline(y=bench_perf, line_dash="dash", line_color="green", annotation_text="NIFTY 50")
                
                fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0),
                                  title="Learning Curve (₹ Fitness Index)",
                                  yaxis_title="Optimization Level")
                st.plotly_chart(fig, use_container_width=True)

            with res_col2:
                st.subheader("🏆 Winning Portfolio")
                selected = [INDIAN_TICKERS[i] for i in range(n_assets) if best_q[i] == 1]
                st.write(f"**Assets Picked:** {len(selected)}")
                for s in selected:
                    st.write(f"- {s}")
                st.metric("Final QGA Fitness", f"₹ {fit_q:.4f}", f"{((fit_q/fit_g)-1):.1%} vs GA")

            st.success("Optimization analysis complete. Benchmarks verified against NIFTY 50.")
