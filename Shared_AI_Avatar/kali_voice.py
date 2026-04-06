import streamlit as st
import asyncio
import edge_tts
import base64
import os
import tempfile
import time

# --- KALI Voice: Voice Profile ---
KALI_VOICE_PROFILE = "en-US-AriaNeural" # or "en-US-JennyNeural"

async def generate_speech_audio(text, voice=KALI_VOICE_PROFILE):
    """Generates KALI's neural voice from text using edge-tts."""
    communicate = edge_tts.Communicate(text, voice)
    
    # Create temp audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    
    return tmp_path

def speak_text(text, placeholder):
    """Renders autoplays audio in streamlit and mutes if necessary."""
    if "kali_mute" not in st.session_state:
        st.session_state.kali_mute = False
        
    if st.session_state.kali_mute:
        return
        
    try:
        # Loop over until file is ready and playable
        # Edge-tts can be async so I'll wrap it
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        path = loop.run_until_complete(generate_speech_audio(text))
        
        with open(path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            
            # Use small invisible audio tag
            audio_tag = f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            placeholder.markdown(audio_tag, unsafe_allow_html=True)
            
        # Optional: cleanup (wait a bit to be safe or delete it)
        # os.unlink(path) 
    except Exception as e:
        st.error(f"KALI Voice Failure: {e}")

def get_voice_transcription():
    """Reserved for future streamlit-audiorecorder integration."""
    # Note: Streamlit-audiorecorder returns audio_bytes or a wav/mp3.
    # To transcribe, we'd typically send to Whisper API or similar.
    # For now, we'll placeholder as requested.
    pass
