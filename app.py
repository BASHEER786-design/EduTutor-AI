# app.py# app.py
import streamlit as st
from ibm_ai import get_ai_response
from fpdf import FPDF
import base64
import os

# --- Function to sanitize text for PDF ---
def sanitize_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

# --- Streamlit Page Config ---
st.set_page_config(page_title="EduTutor AI Search", layout="wide", page_icon="🔍")

# --- Session State for History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Title + Search Box ---
st.markdown(
    "<h1 style='text-align:center'>🔍 EduTutor AI</h1>", unsafe_allow_html=True
)
st.caption("Type any question and get instant answers — like Gemini AI ✨")

# Subject Dropdown
subject = st.selectbox("📚 Subject (optional):", ["General", "Math", "Science", "History", "Technology"], index=0)
instruction = "" if subject == "General" else f"You are an expert in {subject}. "

# Search bar (press Enter to search)
char_limit = 300
user_input = st.text_input(
    "Ask your question:",
    placeholder="e.g. What is Newton's second law?",
    max_chars=char_limit
)

if user_input and len(user_input) > char_limit * 0.9:
    st.warning(f"You're approaching the {char_limit}-character limit.")

# --- Clear History Button ---
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.success("Chat history cleared.")

# --- Instant AI Response ---
if user_input:
    with st.spinner("Thinking..."):
        try:
            full_prompt = instruction + user_input
            response = get_ai_response(full_prompt)

            # Show instant answer card
            st.markdown("### 💡 Instant Answer")
            st.markdown(f"<div style='padding:10px; background-color:#f0f2f6; border-radius:8px;'>{response}</div>", unsafe_allow_html=True)

            # Save to history
            st.session_state.history.append((user_input, response))

        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- History Section ---
if st.session_state.history:
    st.markdown("## 🗂️ Recent Searches")

    for i, (q, a) in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Q{i}: {q}", expanded=False):
            st.markdown(f"**Answer:**\n\n{a}", unsafe_allow_html=True)

            # PDF generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            clean_q = sanitize_text(q)
            clean_a = sanitize_text(a)
            pdf.multi_cell(0, 10, f"Question: {clean_q}\n\nAnswer: {clean_a}")

            pdf_file = f"answer_{i}.pdf"
            try:
                pdf.output(pdf_file)
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()
                    b64 = base64.b64encode(pdf_bytes).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_file}">📄 Download PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                os.remove(pdf_file)
            except Exception as e:
                st.error(f"⚠️ PDF generation failed: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ by basheer | EduTutor AI")

