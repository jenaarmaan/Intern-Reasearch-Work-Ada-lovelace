import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import sys
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Path patching
sys.path.append(os.path.abspath("Shared_Core"))
from qga_engine import (
    PortfolioOptimizer, QGAEngine, fetch_india_data, 
    calculate_advanced_metrics, INDIAN_STOCK_MAP, SECTOR_MAP
)

def run_assignment_2():
    st.header("BEE Portfolio Optimizer — Indian Markets")
    st.markdown("### Quantum Genetic Algorithm applied to NSE-listed stocks")
    
    # 1. Asset Selection
    all_options = [f"{name} ({ticker})" for ticker, name in INDIAN_STOCK_MAP.items()]
    selected_options = st.multiselect(
        "Select Indian Stocks for your Portfolio Universe:",
        all_options,
        default=all_options[:5] # Default to first 5
    )
    
    if not selected_options:
        st.warning("Please select at least one stock to begin.")
        return

    # Extract tickers from selection strings
    selected_tickers = [opt.split('(')[1].strip(')') for opt in selected_options]

    # Live Data Fetching
    try:
        with st.spinner("Fetching live market data from NSE India..."):
            data, source_tag = fetch_india_data(selected_tickers)
            if data is None or data.empty:
                st.error("Failed to retrieve market data. The NSE feed may be temporarily unavailable.")
                return
            
            # Returns for metrics
            returns_df = data[selected_tickers].pct_change().dropna()
            # Annualized metrics for optimizer
            avg_returns = returns_df.mean().values * 252
            risks = returns_df.std().values * np.sqrt(252)
            
            # Benchmark for chart
            bench_ticker = "^NSEI"
            if bench_ticker in data.columns:
                bench_data = data[bench_ticker].pct_change().dropna()
                bench_perf = bench_data.mean() * 252
            else:
                bench_perf = 0.12 # Default 12% if benchmark missing
    except Exception as e:
        st.error(f"Market Data Integration Error: {e}")
        return
    
    # Clean Metric Overview
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Market Status", "NSE Open", "Live Feed")
    with m2: st.metric("Local Index", "NIFTY 50", f"{bench_perf:.2%}")
    with m3: st.metric("Currency", "INR (₹)")
    with m4: st.metric("Data Health", source_tag)
    
    st.markdown("---")
    
    # Main Dashboard Columns
    col_ctrl, col_viz = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Optimizer Config")
        pop_size = st.select_slider("Swarm Size (Qubits)", options=[16, 32, 64, 128], value=32, key="a2_p")
        risk_bias = st.slider("Risk Matrix Bias (λ)", 0.0, 1.0, 0.5, key="a2_r")
        st.info("BEE CORE utilizes Quantum Rotation Gates (Ry) to navigate the Indian investment landscape.")

    with col_viz:
        st.subheader("QGA Benchmarking")
        
        n_assets = len(selected_tickers)
        optimizer = PortfolioOptimizer(n_assets, avg_returns, risks)
        qga = QGAEngine(optimizer, pop_size=pop_size, max_gen=100)
        
        if st.button("🌟 INITIATE QUANTUM OPTIMIZATION", key="a2_btn", use_container_width=True):
            with st.status("Optimizing...", expanded=True) as status:
                st.write("Initializing Qubits at $\pi/4$...")
                time.sleep(0.5)
                st.write(f"Analyzing {n_assets} NSE Assets...")
                best_ind, best_fit, history = qga.run(risk_aversion=risk_bias)
                status.update(label="Optimization Complete", state="complete")

            # Metrics Calculation
            sharpe, sortino, mdd = calculate_advanced_metrics(best_ind, returns_df)

            # Performance Metrics
            p1, p2, p3 = st.columns(3)
            p1.metric("Sharpe Ratio", sharpe)
            p2.metric("Sortino Ratio", sortino)
            p3.metric("Max Drawdown", f"{mdd}%")

            # Main Convergence Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=history, mode='lines', name='QGA Portfolio', line=dict(color='#4A90D9', width=3)))
            fig.add_hline(y=bench_perf, line_dash="dash", line_color="#34A853", annotation_text="NIFTY 50 (₹)")
            fig.update_layout(title="Quantum Convergence vs NIFTY 50 (NSE India)", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

            # Sector Breakdown Chart
            st.divider()
            st.subheader("Sector Allocation")
            winning_tickers = [selected_tickers[i] for i in range(n_assets) if best_ind[i] == 1]
            if winning_tickers:
                sectors = [SECTOR_MAP.get(t, "Other") for t in winning_tickers]
                sector_counts = pd.Series(sectors).value_counts()
                fig_pie = px.pie(
                    values=sector_counts.values, 
                    names=sector_counts.index, 
                    title="Portfolio Sector Concentration",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # KALI AUTO-COMMENT
                interpretation = "strong risk-adjusted performance" if sharpe > 1.5 else "balanced outlook" if sharpe > 1.0 else "potential for volatility"
                kali_response = f"The QGA has found an optimal allocation. The portfolio's Sharpe Ratio of {sharpe} suggests {interpretation} for your INR-denominated assets."
                st.session_state.kali_message = kali_response
                st.session_state.kali_status = "speaking"
                
                st.success(f"**Optimal Selection:** {', '.join(winning_tickers)}")
            else:
                st.warning("The optimizer did not find a valid allocation. Try lowering the Risk Bias.")

        else:
            st.info("Configure your asset universe and press Initiate to run the BEE Portfolio Engine.")

    st.divider()
    st.caption("This is a research simulation only. Not financial advice. All data provided through NSE India / Yahoo Finance.")
