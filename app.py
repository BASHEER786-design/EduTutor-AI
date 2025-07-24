# app.py
import streamlit as st
from ibm_ai import get_ai_response
import pyttsx3
from fpdf import FPDF
import base64

# Page config
st.set_page_config(page_title="EduTutor-AI", layout="centered", page_icon="📘")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📘 EduTutor AI")
st.caption("Ask me any educational question. I'm here to help you learn! 💡")

# Subject selector
subject = st.selectbox("🎓 Choose Subject (optional)", ["General", "Math", "Science", "History", "Technology"])
instruction = "" if subject == "General" else f"You are an expert in {subject}. "

# Text input
char_limit = 300
user_input = st.text_input("🧑‍🎓 Your Question:", placeholder="e.g. What is a binary search algorithm?", max_chars=char_limit)

# Warn on limit
if user_input and len(user_input) > char_limit * 0.9:
    st.warning(f"You're approaching the {char_limit}-character limit.")

# Clear chat
if st.button("🧹 Clear History"):
    st.session_state.history = []
    st.success("Chat history cleared!")

# Generate response
if user_input:
    with st.spinner("Thinking..."):
        try:
            full_prompt = instruction + user_input
            response = get_ai_response(full_prompt)
            st.session_state.history.append((user_input, response))
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Chat history
if st.session_state.history:
    st.subheader("🗂️ Chat History")

    for i, (q, a) in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Q{i}: {q}", expanded=False):
            st.markdown(f"**Answer:**\n\n{a}", unsafe_allow_html=True)
            st.code(a, language="text")

            # PDF Download
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Question: {q}\n\nAnswer: {a}")
            pdf_file = f"answer_{i}.pdf"
            pdf.output(pdf_file)

            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
                b64 = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_file}">📄 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit | EduTutor AI")
