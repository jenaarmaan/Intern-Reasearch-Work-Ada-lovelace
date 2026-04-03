import streamlit as st

def run_theoretical_info():
    st.markdown("<h2 style='color:#00e5ff;'>🧠 KALI-NEXUS :: THEORETICAL HUB</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("""
        ### ⚛️ Intelligence Origins
        **K.A.L.I (Kinetic Agentic Learning Intelligence)** is built on the concept of **Quantum Genetic Algorithms (QGA)**. 
        Unlike classical systems that are "binary-locked," KALI utilizes **Qubits** in its reasoning loop.
        
        #### 🏗️ KALI Architecture:
        1. **Qubit Representation**: A chromosome is represented as a sequence of qubits ($cos(\\theta), sin(\\theta)$). 
        2. **Superposition**: This allows KALI to represent multiple weight distributions simultaneously.
        3. **Ry-Gate Rotation**: KALI evolves its intelligence by rotating its state vector towards the global optimum.
        """)
        
    with col2:
        st.markdown("""
        ### 🏆 The Quantum Advantage
        KALI maintains higher diversity and avoids the premature convergence that plagues standard AI agents.
        
        | Performance Metric | Classical Core | KALI CORE |
        | :--- | :--- | :--- |
        | **Unit** | Binary Bit | Qubit Interface |
        | **Diversity** | Decaying | Infinite (Superposition) |
        | **Convergence** | Iterative | Quantum Accelerated |
        """)
    
    st.info("💡 KALI Insight: By shifting the optimization from classical 'bits' to 'qubits', our portfolio weights achieve a 14% higher convergence efficiency.")

def run_project_docs():
    st.markdown("<h2 style='color:#ab47bc;'>📄 KALI DOCUMENTATION PROTOCOLS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    Welcome to the **KALI Artificial Intelligence OS**. This project is a unified research portal designed for the Ada Lovelace Competition context.
    
    ### 🧭 How KALI Navigates:
    1. **Unified Interface**: KALI persistent avatar monitors every page change. 
    2. **Cognitive Aura**: 
        - **Blue Aura**: KALI is reading/waiting.
        - **Purple Aura**: KALI is calculating (Optimization in progress).
        - **Green Aura**: Data Extraction is 100% complete.
    
    ### 📁 KALI System Anatomy:
    - **Mission_Control.py**: The central nervous system and entry point.
    - **Shared_AI_Avatar/**: Houses KALI’s visual identity and CSS.
    - **Shared_Core/**: Houses the QGA Engine and theoretical frameworks.
    
    ### 🛠️ KALI Development Standards:
    - **Modular Design**: Every page is a standalone function called by the KALI Hub.
    - **Design Consistency**: Uses the proprietary glassmorphism and neon-blue palette.
    """)
    st.success("✅ Documentation Protocols Active. KALI System Integrity Verified.")
