# app.py

import streamlit as st
from ibm_ai import get_ai_response  # Uses OpenAI API internally

# Page config
st.set_page_config(page_title="EduTutor-AI", layout="centered")

st.title("📘 EduTutor AI")
st.write("Ask me any educational question. I'm here to help you learn!")

# Input box for question
user_input = st.text_input("🧑‍🎓 Your Question:", placeholder="e.g. What is a binary search algorithm?")

# Handle response
if user_input:
    with st.spinner("Thinking..."):
        try:
            response = get_ai_response(user_input)
            st.success("Here's the answer:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
