import streamlit as st

def run_avatar_specs():
    st.header("System Architecture")
    st.markdown("---")
    
    # Section 1: All Assignments Overview
    st.subheader("Research Deliverables")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        #### 📄 Assignment 1: Technical Report
        - **Subject:** Agent Architecture Design & Analysis.
        - **Focus:** Comparative study of Devin vs Claude.
        - **Key Framework:** PEAS (Performance, Environment, Actuators, Sensors).
        """)
    with c2:
        st.markdown("""
        #### 🧪 Assignment 2: Quantum Portfolio Optimizer
        - **Subject:** QGA (Quantum Genetic Algorithm) Portfolio Management.
        - **Focus:** Optimized stock weighting using $Ry$-Gate rotations.
        - **Result:** Superior data-convergence over standard PSO/GA.
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Avatar Features & Working
    st.subheader("KALI Assistant Features")
    
    tab1, tab2, tab3 = st.tabs(["💎 Design Characteristics", "⚙️ Operational Logic", "🚀 Proper Working Guidance"])
    
    with tab1:
        st.markdown("""
        - **Professional Persona**: A clean, academic assistant designed for research support.
        - **Status Indicators**: Simple color-coded messages (Blue/Green/Orange) for clear communication.
        - **Modern Layout**: Follows standard educational platform design principles.
        - **Typewriter Rendering**: Clean, readable response generation.
        """)
        
    with tab2:
        st.markdown("""
        - **Module Rendering**: KALI uses an optimized Python engine that injects CSS directly into the Streamlit DOM.
        - **Path Portability**: Asset management using `os.path` for GitHub/Cloud compatibility.
        - **Typewriter Animation**: Character-by-character speech rendering via CSS keyframes.
        """)
        
    with tab3:
        st.markdown("""
        **1. COMMAND**: User selects a page from the navigation menu.
        
        **2. INTEGRATION**: KALI-Core reads the current state and updates the *Session State*.
        
        **3. MANIFESTATION**: The `render_avatar()` function is called to display the visual interface.
        
        **4. EXECUTION**: During computation, KALI updates the status indicator to show processing activity.
        """)

    st.markdown("---")
    st.info("🎯 **KALI SYSTEM STATUS**: All characteristics nominal. Mission Control Integration 100%.")
