import streamlit as st
import os

def run_assignment_1():
    st.markdown("<h1 style='color:#00e5ff;'>📄 TECHNICAL REPORT: AI AGENT ARCHITECTURE</h1>", unsafe_allow_html=True)
    st.markdown("### Agent Architecture Design & Analysis (Assignment 1 Deliverable)")
    
    # Path to report
    report_path = os.path.join("Assignment_1", "Technical_Report.md")
    
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            st.markdown(content)
    else:
        st.error("Technical Report not found in Assignment_1 directory.")
    
    st.markdown("---")
    st.success("✅ Deliverable 1.1: Technical Analysis Report Loaded.")
