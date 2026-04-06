import streamlit as st
import asyncio
import edge_tts
import base64
import os
import tempfile
import time
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# --- KALI Voice Config ---
VOICE = "en-US-AriaNeural"
RATE = "+10%"
PITCH = "+5Hz"

# --- Initialization ---
if "kali_muted" not in st.session_state:
    st.session_state.kali_muted = False
if "voice_queue" not in st.session_state:
    st.session_state.voice_queue = []
if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False

@st.cache_resource(show_spinner=False)
def get_speech_loop():
    """Returns a fresh event loop for TTS generation."""
    return asyncio.new_event_loop()

@st.cache_data(show_spinner=False)
def generate_speech_audio_sync(text):
    """
    Synchronous wrapper for generating KALI's neural voice.
    Cached to ensure the same word results in zero latency for the second instance.
    """
    loop = get_speech_loop()
    asyncio.set_event_loop(loop)
    
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        loop.run_until_complete(communicate.save(tmp_path))
    
    return tmp_path

def speak(text):
    """
    KALI Voice Output Engine.
    Handles caching, queuing, muting, and audio-reactive timing.
    """
    if st.session_state.kali_muted:
        return 0
    
    if st.session_state.is_speaking:
        st.session_state.voice_queue.append(text)
        return
    
    st.session_state.is_speaking = True
    
    try:
        # Use cached sync generator
        path = generate_speech_audio_sync(text)
        
        # Calculate duration approx
        duration = len(text) / 15.0
        
        # Inject Audio
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            audio_tag = f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_tag, unsafe_allow_html=True)
        
        st.session_state.is_speaking = False
        if st.session_state.voice_queue:
            next_text = st.session_state.voice_queue.pop(0)
            speak(next_text)

        return duration
        
    except Exception as e:
        st.error(f"KALI Vocal Node Failure: {e}")
        st.session_state.is_speaking = False
        return 0

def listen():
    """
    KALI Voice Input Engine.
    Uses audio_recorder_streamlit for UI and SpeechRecognition for transcription.
    """
    st.info("KALI Listening Node: Active. Click the microphone icon.")
    audio_bytes = audio_recorder(text="Listen", icon_size="2x")
    
    if audio_bytes:
        # Save raw bytes to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_bytes)
            tmp_path = tmp_audio.name
            
        # Transcribe
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            return "KALI detected silence or unindexed phonemes."
        except sr.RequestError as e:
            return f"Transcription service unavailable: {e}"
        except Exception as e:
            return f"KALI Listening Error: {e}"
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)
    
    return ""

def set_mute(muted_status: bool):
    """Sets KALI's vocal suppression mode."""
    st.session_state.kali_muted = muted_status
