# app.py
import streamlit as st
from ibm_ai import get_ai_response
from fpdf import FPDF
import base64
import os

# Function to sanitize text for PDF (Latin-1 encoding safe)
def sanitize_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

# Page setup
st.set_page_config(page_title="EduTutor-AI", layout="centered", page_icon="📘")

# Session state for chat
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📘 EduTutor AI")
st.caption("Ask any educational question and get instant answers powered by AI 💡")

# Subject dropdown
subject = st.selectbox("📚 Select Subject (optional)", ["General", "Math", "Science", "History", "Technology"])
instruction = "" if subject == "General" else f"You are an expert in {subject}. "

# Character-limited input box
char_limit = 300
user_input = st.text_input("🧑‍🎓 Your Question:", placeholder="e.g. What is Newton's second law?", max_chars=char_limit)

if user_input and len(user_input) > char_limit * 0.9:
    st.warning(f"You're approaching the {char_limit}-character limit.")

# Clear history button
if st.button("🧹 Clear History"):
    st.session_state.history = []
    st.success("Chat history cleared.")

# Get AI response
if user_input:
    with st.spinner("Thinking..."):
        try:
            full_prompt = instruction + user_input
            response = get_ai_response(full_prompt)
            st.session_state.history.append((user_input, response))
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Display chat history
if st.session_state.history:
    st.subheader("🗂️ Chat History")

    for i, (q, a) in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Q{i}: {q}", expanded=False):
            st.markdown(f"**Answer:**\n\n{a}", unsafe_allow_html=True)
            st.code(a, language="text")

            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            clean_q = sanitize_text(q)
            clean_a = sanitize_text(a)
            pdf.multi_cell(0, 10, f"Question: {clean_q}\n\nAnswer: {clean_a}")

            pdf_file = f"answer_{i}.pdf"
            try:
                pdf.output(pdf_file)

                # Encode PDF to base64 for download
                with open(pdf_file, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_file}">📄 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Optional: Remove the file after encoding (to keep Streamlit Cloud clean)
                os.remove(pdf_file)

            except Exception as e:
                st.error(f"PDF generation failed: {e}")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit | EduTutor AI")
