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
        st.session_state.current_questions = get_new_questions()
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {}
    if "show_results" not in st.session_state:
        st.session_state.show_results = False

def get_new_questions():
    remaining_questions = [q for q in quiz_data if q not in st.session_state.answered_questions]
    if len(remaining_questions) < 3:
        st.session_state.answered_questions = []
        remaining_questions = quiz_data
    return random.sample(remaining_questions, 3)

def display_quiz():
    for idx, question in enumerate(st.session_state.current_questions):
        st.subheader(f"Question {idx + 1}:")
        
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
        answer = st.radio("Choose an answer:", options, key=f"q{idx}")
        
        # Store the answer and correct answer for later checking
        st.session_state.current_answers[idx] = {
            'selected': answer,
            'correct': correct_answer,
            'question': question
        }

def main():
    run_quiz()
    
    if not st.session_state.show_results:
        display_quiz()
        
        # Single submit button for all questions
        if st.button("Submit Answers"):
            score = 0
            # Check answers and update score
            for idx, answer_data in st.session_state.current_answers.items():
                if answer_data['selected'] == answer_data['correct']:
                    score += 1
                    st.session_state.answered_questions.append(answer_data['question'])
            
            st.session_state.score += score
            st.session_state.show_results = True
            st.rerun()
    
    else:
        # Display results
        st.subheader("Results:")
        for idx, answer_data in st.session_state.current_answers.items():
            st.write(f"Question {idx + 1}:")
            if answer_data['selected'] == answer_data['correct']:
                st.success(f"Correct! Answer: {answer_data['correct']}")
            else:
                st.error(f"Incorrect. You selected: {answer_data['selected']}")
                st.write(f"Correct answer: {answer_data['correct']}")
        
        st.write(f"Your score for this round: {sum(1 for a in st.session_state.current_answers.values() if a['selected'] == a['correct'])} out of 3")
        st.write(f"Total score: {st.session_state.score}")
        
        # Button to start next round
        if st.button("Next Round"):
            st.session_state.current_questions = get_new_questions()
            st.session_state.current_answers = {}
            st.session_state.show_results = False
            st.rerun()

if __name__ == "__main__":
    main()
