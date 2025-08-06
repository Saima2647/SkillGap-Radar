import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from fpdf import FPDF
import tempfile
import base64
from utils.css import apply_custom_button_style

# load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# load custome css 
apply_custom_button_style()

# Ensure resume exists
if "resume" not in st.session_state or not st.session_state.resume:
    st.warning("⚠️ Missing resume. Please analyze a resume first.")
    st.stop()

resume_text = st.session_state.resume
skills = st.session_state.get("skills", [])

# -------------------------------
# 📝 Edit Resume Section
# -------------------------------
st.subheader("📝 Edit Your Resume Inline")
edited_resume = st.text_area("Edit your full resume below:", resume_text, height=600)
st.session_state.updated_resume = edited_resume  # Store in session for use elsewhere

# -------------------------------
# 💡 AI Suggestions Section
# -------------------------------
st.subheader("💡 AI Suggestions to Improve Resume")
improve_prompt = f"""
You are a resume improvement assistant. Improve grammar, tone, and professionalism of the following resume:

{resume_text}

Return stronger lines, refined grammar, and professional phrasing.
"""

try:
    suggestion = Groq(api_key=api_key).chat.completions.create(
        messages=[{"role": "user", "content": improve_prompt}],
        model="llama3-8b-8192",
    ).choices[0].message.content

    st.session_state.generated_resume = suggestion

    with st.expander("📋 View AI Suggested Resume"):
        st.markdown(suggestion)

except Exception as e:
    st.error(f"⚠️ AI Suggestion Error: {e}")
    suggestion = None

# -------------------------------
# 📥 Download AI Suggested Resume
# -------------------------------
if suggestion and st.button("📄 Download AI Suggested Resume as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=12)

    for line in suggestion.strip().split("\n"):
        try:
            pdf.multi_cell(0, 10, txt=line.encode("latin-1", "replace").decode("latin-1"))
        except:
            continue

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            download_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="AI_Suggested_Resume.pdf">📄 Click to Download AI-Suggested Resume</a>'
            st.markdown(download_link, unsafe_allow_html=True)

# -------------------------------
# 📥 Download Edited Resume
# -------------------------------
if st.button("📥 Download Edited Resume as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=12)

    for line in edited_resume.strip().split("\n"):
        try:
            pdf.multi_cell(0, 10, txt=line.encode("latin-1", "replace").decode("latin-1"))
        except:
            continue

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            download_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="Edited_Resume.pdf">📥 Click to Download Edited Resume</a>'
            st.markdown(download_link, unsafe_allow_html=True)
