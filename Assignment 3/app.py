import streamlit as st
import json
from backend.services.ai_engine import generate_circuit_json
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
    }
    .metric-card {
        background-color: #16161e;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #2d2d39;
        text-align: center;
    }
    .gradient-text {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1>AQC-<span class="gradient-text">GA</span></h1>', unsafe_allow_html=True)
st.caption("AI-Powered Quantum Circuit Generation & Analysis")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Configuration")
    sim_type = st.selectbox("Simulation Mode", ["Ideal (Noise-free)", "Noisy (Coming Soon)"])
    st.info("Powered by Gemini 1.5 Flash & Qiskit")

# Main Input
prompt = st.text_area("Describe your quantum circuit", placeholder="e.g., Create a GHZ state with 3 qubits...")

if st.button("🚀 Generate & Simulate"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Quantum AI is thinking..."):
            # 1. AI Generation
            circuit_json = generate_circuit_json(prompt)
            
            if "error" in circuit_json:
                st.error(f"AI Generation Failed: {circuit_json['error']}")
            else:
                # 2. Correction & Validation
                circuit_json = correct_circuit_json(circuit_json)
                is_valid, v_error = validate_circuit_json(circuit_json)
                
                if not is_valid:
                    st.error(f"Validation Error: {v_error}")
                    st.json(circuit_json)
                else:
                    # 3. Execution
                    result = build_and_simulate_circuit(circuit_json)
                    
                    if not result["success"]:
                        st.error(f"Execution Error: {result['error']}")
                    else:
                        st.success("Circuit Generated Successfully!")
                        
                        # --- Results Display ---
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.metric("Depth", result["metrics"]["depth"])
                            st.markdown('</div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.metric("Gate Count", result["metrics"]["gate_count"])
                            st.markdown('</div>', unsafe_allow_html=True)
                        with col3:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.metric("Width", result["metrics"]["width"])
                            st.markdown('</div>', unsafe_allow_html=True)

                        # Simulation Results Chart
                        st.subheader("📊 Simulation Probabilities")
                        counts = result["results"]
                        total_shots = sum(counts.values())
                        probs = {f"|{k}⟩": v/total_shots for k, v in counts.items()}
                        st.bar_chart(probs)

                        # Expanders for code/data
                        with st.expander("📝 View Circuit JSON (IR)"):
                            st.json(circuit_json)
                        
                        with st.expander("⚛️ View QASM Code"):
                            st.code(result["qasm"], language="qasm")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #555;">Built with ❤️ for Quantum Research</div>', unsafe_allow_html=True)
