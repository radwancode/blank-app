import streamlit as st
import random
from quiz_data import quiz_data

def run_quiz():
    st.title("Geography Quiz Time!")

    # Initialize session state
    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = []
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_questions" not in st.session_state:
        st.session_state.current_questions = []
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {}
    if "questions_answered_this_round" not in st.session_state:
        st.session_state.questions_answered_this_round = 0

    # Get new questions if we don't have any
    if not st.session_state.current_questions:
        remaining_questions = [q for q in quiz_data if q not in st.session_state.answered_questions]
        if len(remaining_questions) < 3:
            st.session_state.answered_questions = []
            remaining_questions = quiz_data
        st.session_state.current_questions = random.sample(remaining_questions, 3)
        st.session_state.questions_answered_this_round = 0

    # Display questions
    for idx, question in enumerate(st.session_state.current_questions):
        st.subheader(f"Question {idx + 1}:")
        
        # Skip if already answered in this round
        if question.get('answered_in_round', False):
            st.info(f"Answered correctly! {question.get('feedback', '')}")
            continue

        category = random.choice(['capital', 'border_countries', 'water_bodies', 'interesting_facts'])
        
        if category == 'capital':
            correct_answer = question['capital']
            options = [question['capital']] + random.sample([q['capital'] for q in quiz_data if q != question], 3)
            st.write(f"What is the capital of {question['country']}?")
        elif category == 'border_countries':
            correct_answer = ', '.join(question['border_countries'])
            options = [', '.join(question['border_countries'])] + random.sample(
                [', '.join(q['border_countries']) for q in quiz_data if q != question], 3)
            st.write(f"Which countries border {question['country']}?")
        elif category == 'water_bodies':
            correct_answer = ', '.join(question['water_bodies'])
            options = [', '.join(question['water_bodies'])] + random.sample(
                [', '.join(q['water_bodies']) for q in quiz_data if q != question], 3)
            st.write(f"What water bodies are found near {question['country']}?")
        else:  # interesting_facts
            correct_answer = random.choice(question['interesting_facts'])
            options = [correct_answer] + random.sample(
                [random.choice(q['interesting_facts']) for q in quiz_data if q != question], 3)
            st.write(f"Which of the following is an interesting fact about {question['country']}?")

        random.shuffle(options)
        
        # Create columns for answer and submit button
        col1, col2 = st.columns([3, 1])
        
        with col1:
            answer = st.radio("Choose an answer:", options, key=f"q{idx}")
        
        with col2:
            if st.button("Submit", key=f"submit{idx}"):
                if answer == correct_answer:
                    st.session_state.score += 1
                    st.session_state.questions_answered_this_round += 1
                    question['answered_in_round'] = True
                    question['feedback'] = f"The correct answer is: {correct_answer}"
                    st.session_state.answered_questions.append(question)
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct answer is: {correct_answer}")
                st.rerun()

    # Show progress
    st.write(f"Current score: {st.session_state.score}")
    
    # Check if all questions in current round are answered
    if st.session_state.questions_answered_this_round == 3:
        if st.button("Next Round"):
            st.session_state.current_questions = []
            st.session_state.current_answers = {}
            st.session_state.questions_answered_this_round = 0
            st.rerun()

if __name__ == "__main__":
    run_quiz()
