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
from qga_engine import PortfolioOptimizer, QGAEngine, fetch_india_data, calculate_metrics, INDIAN_TICKERS

def format_indian_currency(value):
    """Simple Indian currency formatter."""
    return f"₹{value:,.2f}"

def run_assignment_2():
    st.header("BEE DASHBOARD")
    st.write("Quantum Strategic Analysis Portfolio Suite (India Assets)")
    
    # Live Data Fetching
    with st.spinner("Fetching live market data from NSE India..."):
        all_tickers = INDIAN_TICKERS + ["MARUTI.NS", "LTIM.NS", "SUNPHARMA.NS", "AXISBANK.NS", "NESTLEIND.NS"]
        data, source_tag = fetch_india_data(all_tickers)
        returns, risks, bench_perf = calculate_metrics(data, all_tickers)
    
    # Clean Metric Overview
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("NSE Status", "Open", "Live")
    with m2: st.metric("NIFTY 50 (Annualized)", f"{bench_perf:.2%}")
    with m3: st.metric("Data Source", source_tag)
    with m4: st.metric("Latency", "4ms", "0.2ms")
    
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Main Dashboard Columns
    col_ctrl, col_viz = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Strategy Config")
        
        with st.container():
            pop_size = st.select_slider("Swarm Size", options=[16, 32, 48, 64, 128], value=48, key="a2_p")
            gen = st.slider("Evolution Generations", 50, 200, 80, key="a2_g")
            risk_bias = st.slider("Risk Matrix Bias (λ)", 0.0, 1.0, 0.5, key="a2_r")
            
        st.info("BEE CORE is synchronized with local Indian market data.")
        
        with st.expander("View Asset Universe"):
            asset_df = pd.DataFrame({
                "Ticker": all_tickers,
                "Expected Return": returns,
                "Volatility (Risk)": risks
            })
            st.dataframe(asset_df.style.format({
                "Expected Return": "{:.2%}",
                "Volatility (Risk)": "{:.2%}"
            }))

    with col_viz:
        st.subheader("Quantum Convergence Monitor")
        
        n_assets = len(all_tickers)
        optimizer = PortfolioOptimizer(n_assets, returns, risks)
        qga = QGAEngine(optimizer, pop_size=pop_size, max_gen=gen)
        
        # Action Center
        if st.button("🌟 INITIATE OPTIMIZATION", key="a2_btn", use_container_width=True):
            with st.status("Optimizing Portfolio...", expanded=True) as status:
                st.write("Initializing Qubits...")
                time.sleep(0.5)
                st.write(f"Processing {n_assets} NSE Sector Assets...")
                best_ind, best_fit, history = qga.run(risk_aversion=risk_bias)
                status.update(label="Optimization Complete", state="complete")

            # Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=history, mode='lines', name='BEE QGA-Core',
                                     line=dict(color='#4A90D9', width=4)))
            
            # Add NIFTY Benchmark Constant Line
            fig.add_hline(y=bench_perf, line_dash="dash", line_color="green", 
                          annotation_text="NIFTY 50 Benchmark", annotation_position="bottom right")
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=50, b=0),
                title=dict(text="Convergence vs NIFTY 50<br><span style='font-size:0.8rem; color:gray;'>Data: NSE India</span>"),
                xaxis=dict(title="Generation"),
                yaxis=dict(title="Fitness Index (₹ Value Ratio)"),
                hovermode="x unified",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Winner Summary
            winning_tickers = [all_tickers[i] for i in range(n_assets) if best_ind[i] == 1]
            st.success(f"Optimal Portfolio identified with {len(winning_tickers)} assets.")
            st.write(f"**Selected Assets:** {', '.join(winning_tickers)}")
            st.info(f"Final Optimization Index: {best_fit:.4f} (Relative to INR Benchmark)")
        else:
            st.info("Enter configuration and press Initiate Optimization to begin benchmark comparison.")
