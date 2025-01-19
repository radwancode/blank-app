import streamlit as st
import random
from quiz_data import questions

# Quiz Logic
def run_quiz():
    st.title("Random Quiz Time!")
    
    # Initialize session state to store the answered questions and score
    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = []
    
    if "score" not in st.session_state:
        st.session_state.score = 0
    
    total_questions = len(questions)
    
    # Randomly select 3 questions that have not been answered
    remaining_questions = [q for q in questions if q not in st.session_state.answered_questions]
    
    if len(remaining_questions) == 0:
        st.session_state.answered_questions = []  # Reset the answered questions if all have been answered
        remaining_questions = questions  # Reuse all questions
    
    selected_questions = random.sample(remaining_questions, 3)

    score = 0
    for idx, question in enumerate(selected_questions):
        st.subheader(f"Question {idx + 1}: {question['question']}")
        
        # Radio buttons for choices
        answer = st.radio("Choose an answer:", question['options'], key=f"q{idx}")
        
        # Check if the selected answer is correct
        if answer == question['answer']:
            score += 1
            # Add question to answered questions list
            st.session_state.answered_questions.append(question)
    
    # Display the result after the quiz is completed
    if st.button("Submit Quiz"):
        st.write(f"Your score: {score} out of 3")
        
        if score == 3:
            st.success("You got all the answers correct!")
            # Option to try again with new set of random questions
            if st.button("Next Set of Questions"):
                st.session_state.score += score  # Keep track of the total score
                run_quiz()  # Recursively run the quiz with new questions
        else:
            st.warning(f"You got {score} correct! Try again.")
        
if __name__ == "__main__":
    run_quiz()
