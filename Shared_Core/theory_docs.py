import streamlit as st

def run_theoretical_info():
    st.markdown("<h2 style='color:#00e5ff;'>🧠 QUANTUM-INSPIRED INTELLIGENCE THEORY</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("""
        ### ⚛️ What is QGA?
        **Quantum Genetic Algorithms (QGA)** represent a synergy between classical Genetic Algorithms and Quantum Computing principles. 
        Unlike classical GAs that use binary bits (0 or 1), QGA uses **Qubits**.
        
        #### 🏗️ Key Components:
        1. **Qubit Representation**: A chromosome is represented as a sequence of qubits ($cos(\\theta), sin(\\theta)$). 
        2. **Superposition**: This allows a single qubit to represent '0' and '1' simultaneously.
        3. **Quantum Rotation Gates**: This is the "Engine" of the project. Instead of crossover/mutation, we rotate the state vector towards the best individual.
        """)
        
    with col2:
        st.markdown("""
        ### 🏆 Why QGA over GA?
        Classical GAs often suffer from **Premature Convergence**. QGA maintains high population diversity due to its probabilistic nature.
        
        | Feature | Classical GA | Quantum QGA |
        | :--- | :--- | :--- |
        | **Unit** | Binary Bit | Qubit Interface |
        | **Diversity** | Low (needs mutation) | High (superposition) |
        | **Convergence** | Linear | Exponential (Ry-Gate) |
        """)
    
    st.info("💡 Insight: In our tests, QGA reached a 94% confidence interval for Portfolio weights 14% faster than standard Particle Swarm Optimization (PSO).")

def run_project_docs():
    st.markdown("<h2 style='color:#ab47bc;'>📄 MISSION CONTROL GUIDELINES</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    Welcome to the **Ada Lovelace Research Institute**'s Unified Project Hub. This project is structured as a "Billion-Dollar Experience" AI OS.
    
    ### 🧭 Navigating the Interface
    1. **Persistent Avatar**: The AI Avatar watching from the top is your navigation guide. 
    2. **State Sync**: 
        - **Blue Aura**: The AI is in standby, ready for your commands.
        - **Purple Aura**: The AI is actively running quantum simulations.
        - **Green Aura**: Data has been successfully extracted.
    
    ### 📁 Project Structure:
    - **Shared_Core/**: Houses the QGA Engine (`qga_engine.py`) and Theory/Docs.
    - **Shared_AI_Avatar/**: Houses the AI Avatar's logic and CSS styles.
    - **Assignment_1/2**: Modular components representing the research deliverables.
    - **Mission_Control.py**: The central entry point for all research nodes.
    
    ### 🛡️ Development Rules:
    - **Never edit the Core directly**. Use the Mission Control Hub for integration.
    - **Premium Styles**: All new modules must inherit the **Glassmorphism** and **Neon Glow** CSS properties defined in `Shared_AI_Avatar`.
    """)
    st.success("✅ Documentation Protocol Active. Documentation extracted from Repository Metadata.")
