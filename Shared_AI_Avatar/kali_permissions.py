import streamlit as st

def check_permission(feature: str) -> bool:
    """
    Checks if the user has granted permission for a specific feature (e.g., 'voice').
    If no decision has been made, it renders a consent UI and returns False.
    """
    permission_key = "permission_" + feature
    
    # 1. Check if decision already exists in session state
    current_status = st.session_state.get(permission_key)
    
    if current_status is True:
        return True
    
    if current_status is False:
        return False
        
    # 2. Status is None -> Show Consent UI
    st.markdown("---")
    with st.container():
        st.warning(f"🔔 **Permission Required: {feature.capitalize()} Interaction**")
        st.write(f"KALI would like to use your **{feature}** systems to enable voice input and output.")
        st.write("This allows for a hands-free research experience and real-time audio feedback.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, allow", key=f"perm_allow_{feature}", use_container_width=True):
                st.session_state[permission_key] = True
                st.rerun()
        with col2:
            if st.button("❌ No thanks, skip", key=f"perm_deny_{feature}", use_container_width=True):
                st.session_state[permission_key] = False
                st.info("No problem! You can use all features through text instead.")
                st.rerun()
                
    return False

def render_permission_sidebar():
    """Renders the permission toggles in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Permissions")
    
    # Voice Permission Toggle
    voice_perm = st.session_state.get("permission_voice", False)
    new_val = st.sidebar.toggle("Enable Voice (Mic/TTS)", value=voice_perm, key="sidebar_voice_toggle")
    
    if new_val != voice_perm:
        st.session_state["permission_voice"] = new_val
        st.rerun()

def get_permission_pill(feature: str):
    """Returns a status pill string based on permission state."""
    status = st.session_state.get("permission_" + feature, False)
    if status:
        return f"<span style='color: #34A853; font-weight: bold;'>[Voice: ON]</span>"
    else:
        return f"<span style='color: #ea4335; font-weight: bold;'>[Voice: OFF]</span>"
