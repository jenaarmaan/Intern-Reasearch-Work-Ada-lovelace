import streamlit as st

def run_avatar_specs():
    st.markdown("<h2 style='color:#00f2ff;'>🛡️ KALI CORE :: SYSTEM ARCHITECTURE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Section 1: All Assignments Overview
    st.markdown("### 🛰️ RESEARCH DELIVERABLES HUB")
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
    st.markdown("### 🤖 KALI AVATAR :: FEATURES & LOGIC")
    
    tab1, tab2, tab3 = st.tabs(["💎 Design Characteristics", "⚙️ Operational Logic", "🚀 Proper Working Guidance"])
    
    with tab1:
        st.markdown("""
        - **3D Neural Orb**: A base64-encoded holographic centerpiece for low-latency visual persistence.
        - **Aura Synchronization**: Dynamic CSS shift between Blue (Idle), Purple (Processing), and Green (Success).
        - **Glassmorphic Deck**: 40px backdrop blur with a saturating container for high-end MNC aesthetics.
        - **Laser-Scan Protocol**: Vertical scan beam for simulated activity during idle modes.
        """)
        
    with tab2:
        st.markdown("""
        - **Module Rendering**: KALI uses an optimized Python engine that injects CSS directly into the Streamlit DOM.
        - **Path Portability**: Asset management using `os.path` for GitHub/Cloud compatibility.
        - **Typewriter Animation**: Character-by-character speech rendering via CSS keyframes.
        """)
        
    with tab3:
        st.markdown("""
        **1. COMMAND**: User selects a mission node from the NAVIGATION NEXUS.
        
        **2. INTEGRATION**: KALI-Core reads the mission state and updates the *Session State*.
        
        **3. MANIFESTATION**: The `render_ai_avatar()` function is called with the specific message.
        
        **4. EXECUTION**: During heavy QGA computation, KALI automatically shifts the Aura to **Processing (Purple)** to alert the user of background reasoning.
        """)

    st.markdown("---")
    st.info("🎯 **KALI SYSTEM STATUS**: All characteristics nominal. Mission Control Integration 100%.")
