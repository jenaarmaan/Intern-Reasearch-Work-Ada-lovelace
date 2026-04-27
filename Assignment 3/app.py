import streamlit as st
import json
from backend.services.ai_engine import generate_circuit_json, explain_circuit
from backend.services.quantum_engine import build_and_simulate_circuit
from backend.services.validator import validate_circuit_json, correct_circuit_json

# Page Config
st.set_page_config(
    page_title="AQC-GA | Quantum AI",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #0a0a0c;
    }
    .stTextArea textarea {
        background-color: #16161e;
        color: #f8fafc;
        border-radius: 10px;
        border: 1px solid #3b82f6;
        font-size: 1.1rem;
    }
    .metric-card {
        background-color: #16161e;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #2d2d39;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }
    .gradient-text {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .explanation-box {
        background-color: rgba(59, 130, 246, 0.05);
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1>AQC-<span class="gradient-text">GA</span></h1>', unsafe_allow_html=True)
st.caption("Quantum Circuit Generation & Analysis Platform")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    sim_type = st.selectbox("Simulation Mode", ["Ideal (Noise-free)", "Noisy (Coming Soon)"])
    shots = st.slider("Number of Shots", 100, 4000, 1024)
    st.markdown("---")
    st.markdown("### 🛠️ Status")
    st.success("AI Engine: Online")
    st.success("Quantum Engine: Online")

# Main Interface
col_main, col_info = st.columns([2, 1])

with col_main:
    prompt = st.text_area("What quantum experiment would you like to build?", 
                         placeholder="e.g., Create a Bell state and measure both qubits...",
                         height=120)
    
    gen_btn = st.button("🚀 Generate & Execute", use_container_width=True)

with col_info:
    st.markdown("### 💡 Quick Tips")
    st.markdown("- Be specific about qubit counts.")
    st.markdown("- Mention gates like H, CNOT, or RX.")
    st.markdown("- Ask for 'measurement' to see results.")

if gen_btn:
    if not prompt:
        st.warning("Please describe your circuit first.")
    else:
        with st.spinner("AI is architecting your circuit..."):
            # 1. AI Generation
            circuit_json = generate_circuit_json(prompt)
            
            if "error" in circuit_json:
                st.error(f"Generation Failed: {circuit_json['error']}")
                if "raw" in circuit_json:
                    with st.expander("Debug Details"):
                        st.code(circuit_json["raw"])
            else:
                # 2. Correction & Validation
                circuit_json = correct_circuit_json(circuit_json)
                is_valid, v_error = validate_circuit_json(circuit_json)
                
                if not is_valid:
                    st.error(f"Validation failed: {v_error}")
                else:
                    # 3. Execution & Explanation
                    col_exec, col_expl = st.columns([2, 1])
                    
                    with st.spinner("Simulating on Quantum Engine..."):
                        result = build_and_simulate_circuit(circuit_json)
                        explanation = explain_circuit(prompt, circuit_json)
                    
                    if result["success"]:
                        # Metrics Row
                        m1, m2, m3, m4 = st.columns(4)
                        with m1:
                            st.markdown(f'<div class="metric-card"><h4>Depth</h4><h2 style="color:#8b5cf6;">{result["metrics"]["depth"]}</h2></div>', unsafe_allow_html=True)
                        with m2:
                            st.markdown(f'<div class="metric-card"><h4>Gates</h4><h2 style="color:#3b82f6;">{result["metrics"]["gate_count"]}</h2></div>', unsafe_allow_html=True)
                        with m3:
                            st.markdown(f'<div class="metric-card"><h4>Qubits</h4><h2 style="color:#10b981;">{result["metrics"]["qubits"]}</h2></div>', unsafe_allow_html=True)
                        with m4:
                            st.markdown(f'<div class="metric-card"><h4>Method</h4><p style="font-size:0.8rem;">{result["metrics"]["sim_method"]}</p></div>', unsafe_allow_html=True)

                        # AI Explanation
                        st.markdown(f'<div class="explanation-box"><b>AI Insight:</b><br/>{explanation}</div>', unsafe_allow_html=True)

                        # Visualization Tab
                        tab1, tab2, tab3 = st.tabs(["📊 Simulation", "📐 Circuit Diagram", "📄 Technical Data"])
                        
                        with tab1:
                            st.subheader("Probability Distribution")
                            counts = result["counts"]
                            total = sum(counts.values())
                            probs = {f"|{k}⟩": v/total for k, v in counts.items()}
                            st.bar_chart(probs, color="#3b82f6")
                        
                        with tab2:
                            st.subheader("Circuit Architecture")
                            st.code(result["diagram"], language="text")
                        
                        with tab3:
                            c_json, c_qasm = st.columns(2)
                            with c_json:
                                st.markdown("#### JSON IR")
                                st.json(circuit_json)
                            with c_qasm:
                                st.markdown("#### QASM 2.0")
                                st.code(result["qasm"], language="qasm")
                    else:
                        st.error(f"Execution Failed: {result['error']}")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #444;">AQC-GA v1.1 | Built on Google Gemini & IBM Qiskit</div>', unsafe_allow_html=True)
