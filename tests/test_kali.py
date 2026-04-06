import time
import os
import sys

# --- Mock Path Integration ---
sys.path.append(os.path.abspath("Shared_AI_Avatar"))
sys.path.append(os.path.abspath("Shared_Core"))

def test_integration():
    """
    KALI SYSTEM INTEGRITY TEST
    Verifies all critical AI nodes are synchronous and functional.
    """
    print("--- [KALI_TEST_SUITE] :: INITIATING... ---")
    
    # 1. BRAIN NODE: LLM Response Timing
    try:
        from kali_brain import ask_kali
        start = time.time()
        print("Testing Brain Node (Groq API)...")
        # Sample response
        list(ask_kali("Unit test signal. Are systems nominal?", context="General"))
        elapsed = time.time() - start
        if elapsed < 3.0:
            print(f"✅ Brain Node Optimal: Latency {elapsed:.2f}s")
        else:
            print(f"⚠️ Brain Node Latency HIGH: {elapsed:.2f}s")
    except Exception as e:
        print(f"❌ Brain Node FAIL: {e}")

    # 2. VOICE NODE: TTS Generation Speed
    try:
        from kali_voice import generate_speech_audio
        import asyncio
        print("Testing Voice Node (Edge-TTS)...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        path = loop.run_until_complete(generate_speech_audio("This is a 50-word test to ensure high-speed phoneme generation for the KALI OS mission control. System is now calculating optimal voice rate and pitch values to ensure maximum auditability."))
        if os.path.exists(path):
            print(f"✅ Voice Node Optimal: Localized at {path}")
        else:
            print("❌ Voice Node FAIL: File not generated.")
    except Exception as e:
        print(f"❌ Voice Node FAIL: {e}")

    # 3. PROACTIVE NODE: Trigger Validation
    try:
        from kali_proactive import get_time_greeting
        print("Testing Proactive Node (Triggers)...")
        greeting = get_time_greeting()
        if "Good" in greeting:
            print(f"✅ Proactive Node Optimal: Correct greeting fired ({greeting})")
        else:
            print("❌ Proactive Node FAIL: Incorrect logical evaluation.")
    except Exception as e:
        print(f"❌ Proactive Node FAIL: {e}")

    # 4. ERROR BOUNDARY: safe_run Verification
    try:
        from kali_proactive import safe_run
        print("Testing Error Boundary (Safe-Run)...")
        def broken_fn(): raise ValueError("Intentional Unit Test Crash")
        # safe_run should handle this without breaking the test suite
        safe_run(broken_fn)
        print("✅ Error Boundary Optimal: Trap confirmed.")
    except Exception as e:
        print(f"❌ Error Boundary FAIL: {e}")

    print("--- [KALI_TEST_SUITE] :: COMPLETE ---")

if __name__ == "__main__":
    test_integration()
