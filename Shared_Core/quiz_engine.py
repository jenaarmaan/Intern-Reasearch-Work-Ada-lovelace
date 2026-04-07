import streamlit as st
from quantum_curriculum import CURRICULUM

def render_quiz(topic_key: str):
    """
    Renders an interactive quiz for the specified quantum topic.
    Includes scoring logic and KALI reactions.
    """
    if topic_key not in CURRICULUM:
        return

    topic = CURRICULUM[topic_key]
    quiz_data = topic.get("quiz", [])
    challenge_data = topic.get("challenge", None)

    if not quiz_data:
        st.info("No quiz available for this topic yet.")
        return

    st.markdown("---")
    st.subheader(f"🧠 Quiz: {topic['title']}")
    
    # Initialize session state for quiz
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = {}
    
    # Submission check
    is_submitted = st.session_state.quiz_submitted.get(topic_key, False)

    with st.form(key=f"form_{topic_key}"):
        user_answers = []
        for idx, q_item in enumerate(quiz_data):
            st.write(f"**Q{idx+1}: {q_item['question']}**")
            ans = st.radio(
                f"Select option for Q{idx+1}:", 
                q_item['options'], 
                key=f"radio_{topic_key}_{idx}",
                label_visibility="collapsed"
            )
            user_answers.append(ans)
        
        submit_button = st.form_submit_button(label="📝 Submit Final Answers")

        if submit_button:
            st.session_state.quiz_submitted[topic_key] = True
            st.rerun()

    # Results Processing
    if is_submitted:
        score = 0
        for idx, q_item in enumerate(quiz_data):
            user_ans = st.session_state.get(f"radio_{topic_key}_{idx}")
            correct_ans = q_item['options'][q_item['answer']]
            
            if user_ans == correct_ans:
                score += 1
                st.success(f"Q{idx+1}: Correct! — *{correct_ans}*")
            else:
                st.error(f"Q{idx+1}: Incorrect. The correct answer was: *{correct_ans}*")
        
        # Mastery Calculation
        mastery = score / len(quiz_data)
        st.write(f"### Your Score: {score} out of {len(quiz_data)}")
        
        # KALI Response Dispatch
        kali_msg = ""
        if score == 3:
            kali_msg = "Excellent! You have mastered this concept. You are ready for the challenge!"
            st.session_state.topic_progress[topic_key] = "green"
        elif score == 2:
            kali_msg = "Good effort! Review the lesson once more to get a perfect score."
            st.session_state.topic_progress[topic_key] = "blue"
        else:
            kali_msg = "Let us go through this together. I will explain it again in the chat if you have questions."
            st.session_state.topic_progress[topic_key] = "blue"
        
        st.session_state.kali_message = kali_msg
        st.session_state.kali_status = "speaking"
        
        # Bonus Challenge Logic
        if score == 3 and challenge_data:
            st.markdown("---")
            st.markdown("### 🏆 BONUS CHALLENGE")
            st.write(f"**{challenge_data['question']}**")
            c_ans = st.radio("Challenge Answer:", challenge_data['options'], key=f"challenge_{topic_key}")
            if st.button("Check Challenge Paper"):
                if challenge_data['options'].index(c_ans) == challenge_data['answer']:
                    st.balloons()
                    st.success("INCREDIBLE! You are a Quantum Pioneer!")
                else:
                    st.warning("Almost! That was a tricky one.")

        # Retry Button
        if st.button("🔄 Try Quiz Again"):
            st.session_state.quiz_submitted[topic_key] = False
            st.rerun()
