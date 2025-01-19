import streamlit as st
from quiz_data import questions

# Quiz Logic
def run_quiz():
    st.title("Quiz Time!")
    
    score = 0
    total_questions = len(questions)
    
    for idx, question in enumerate(questions):
        st.subheader(f"Question {idx + 1}: {question['question']}")
        
        # Radio buttons for choices
        answer = st.radio("Choose an answer:", question['options'], key=f"q{idx}")
        
        # Check if the selected answer is correct
        if answer == question['answer']:
            score += 1
            
    # Display the result after the quiz is completed
    if st.button("Submit Quiz"):
        st.write(f"Your score: {score} out of {total_questions}")
        
        if score == total_questions:
            st.success("You got all the answers correct!")
        else:
            st.warning(f"You got {score} out of {total_questions} correct.")

if __name__ == "__main__":
    run_quiz()
