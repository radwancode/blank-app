import streamlit as st
import random
from quiz_data import quiz_data  # Ensure you import the dataset correctly

# Quiz Logic
def run_quiz():
    st.title("Geography Quiz Time!")

    # Initialize session state to store the answered questions and score
    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = []

    if "score" not in st.session_state:
        st.session_state.score = 0

    # Randomly select 3 questions that have not been answered
    remaining_questions = [q for q in quiz_data if q not in st.session_state.answered_questions]
    
    if len(remaining_questions) == 0:
        st.session_state.answered_questions = []  # Reset the answered questions if all have been answered
        remaining_questions = quiz_data  # Reuse all questions
    
    selected_questions = random.sample(remaining_questions, 3)

    answers = []  # To store user answers for review
    question_data = []  # To store the question content for later

    for idx, question in enumerate(selected_questions):
        st.subheader(f"Question {idx + 1}:")
        
        # Randomly pick a category for each question (capital, border_countries, water_bodies, interesting_facts)
        category = random.choice(['capital', 'border_countries', 'water_bodies', 'interesting_facts'])
        
        if category == 'capital':
            correct_answer = question['capital']
            options = [question['capital']] + random.sample([q['capital'] for q in quiz_data if q != question], 3)
            random.shuffle(options)
            st.write(f"What is the capital of {question['country']}?")
        
        elif category == 'border_countries':
            correct_answer = ', '.join(question['border_countries'])
            options = [', '.join(question['border_countries'])] + random.sample(
                [', '.join(q['border_countries']) for q in quiz_data if q != question], 3)
            random.shuffle(options)
            st.write(f"Which countries border {question['country']}?")
        
        elif category == 'water_bodies':
            correct_answer = ', '.join(question['water_bodies'])
            options = [', '.join(question['water_bodies'])] + random.sample(
                [', '.join(q['water_bodies']) for q in quiz_data if q != question], 3)
            random.shuffle(options)
            st.write(f"What water bodies are found near {question['country']}?")
        
        elif category == 'interesting_facts':
            correct_answer = random.choice(question['interesting_facts'])
            options = [correct_answer] + random.sample(
                [random.choice(q['interesting_facts']) for q in quiz_data if q != question], 3)
            random.shuffle(options)
            st.write(f"Which of the following is an interesting fact about {question['country']}?")
        
        # Radio buttons for choices
        answer = st.radio("Choose an answer:", options, key=f"q{idx}")
        
        # Store answer and question data for later use
        answers.append((answer, correct_answer, question))
        question_data.append(question)

    # After all three questions have been answered, submit the answers and display score
    if st.button("Submit Quiz"):
        score = 0  # Reset score for this round

        for answer, correct_answer, question in answers:
            if answer == correct_answer:
                score += 1
                # Mark this question as answered correctly
                if question not in st.session_state.answered_questions:
                    st.session_state.answered_questions.append(question)
        
        st.write(f"Your score for this set: {score} out of 3")
        
        if score == 3:
            st.success("You got all the answers correct!")
        else:
            st.warning(f"You got {score} correct. Try again.")
        
        # Option to continue to the next set of random questions
        st.session_state.score += score  # Keep track of total score

        # Reset score for next round and proceed to next set of questions
        if st.button("Next Set of Questions"):
            run_quiz()  # Recursively run the quiz with new questions

if __name__ == "__main__":
    run_quiz()
