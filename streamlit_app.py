import streamlit as st
import json
import random

# Load the JSON data
with open("quiz_data.py", "r") as file:
    data = json.load(file)

# Initialize session state variables
if "score" not in st.session_state:
    st.session_state.score = {"correct": 0, "total": 0}
if "current_questions" not in st.session_state:
    st.session_state.current_questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Function to generate random questions
def generate_questions():
    st.session_state.current_questions = random.sample(data, 3)
    st.session_state.user_answers = {}
    st.session_state.submitted = False

# Function to reset the quiz
def reset_quiz():
    st.session_state.score = {"correct": 0, "total": 0}
    generate_questions()

# Generate questions if none are loaded
if not st.session_state.current_questions:
    generate_questions()

# Display the quiz title
st.title("Country Quiz")

# Display the current score
st.write(f"Score: {st.session_state.score['correct']}/{st.session_state.score['total']} "
         f"({(st.session_state.score['correct'] / st.session_state.score['total'] * 100 if st.session_state.score['total'] > 0 else 0):.2f}%)")

# Display the questions and collect answers
for i, country_data in enumerate(st.session_state.current_questions):
    st.subheader(f"Question {i + 1}")
    question_type = random.choice(["capital", "border_countries"])
    
    if question_type == "capital":
        st.write(f"What is the capital of {country_data['country']}?")
        st.session_state.user_answers[f"q{i}"] = st.text_input(f"Your answer for {country_data['country']}'s capital:", key=f"q{i}")
    else:
        st.write(f"Name one of the border countries of {country_data['country']}:")
        st.session_state.user_answers[f"q{i}"] = st.text_input(f"Your answer for {country_data['country']}'s border country:", key=f"q{i}")

# Submit button
if st.button("Submit"):
    st.session_state.submitted = True
    all_correct = True

    for i, country_data in enumerate(st.session_state.current_questions):
        question_type = "capital" if "capital" in st.session_state.user_answers[f"q{i}"].lower() else "border_countries"
        user_answer = st.session_state.user_answers[f"q{i}"].strip().lower()

        if question_type == "capital":
            correct_answer = country_data["capital"].lower()
        else:
            correct_answer = [bc.lower() for bc in country_data["border_countries"]]

        if (question_type == "capital" and user_answer == correct_answer) or \
           (question_type == "border_countries" and user_answer in correct_answer):
            st.success(f"Question {i + 1} is correct!")
        else:
            st.error(f"Question {i + 1} is incorrect. The correct answer was: {correct_answer if question_type == 'capital' else ', '.join(correct_answer)}")
            all_correct = False

    if all_correct:
        st.session_state.score["correct"] += 3
        st.session_state.score["total"] += 3
        st.balloons()
        st.write("All answers are correct! Moving to the next set of questions.")
        generate_questions()
    else:
        st.session_state.score["total"] += 3

# Reset button
if st.button("Reset Quiz"):
    reset_quiz()

# Display the current questions for debugging (optional)
# st.write("Current Questions:", st.session_state.current_questions)
