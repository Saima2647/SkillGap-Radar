import streamlit as st


st.header("SkillGap Radar 🎯")

st.title("🧠 About This Project it is an AI Resume Analyzer")


about_text = """
Welcome to **SkillGap Radar 🎯**, your intelligent career companion designed to transform the way you build and evaluate resumes. Whether you're a student, a job seeker, or a working professional, this tool helps you understand how your resume aligns with your dream job — and what you're missing.

🚀 **Core Features**:
- 📄 Analyze your resume against any job description  
- 🤖 AI-generated detailed evaluation and ATS scoring  
- ❌ Detect missing technical/domain skills  
- 📚 Identifies missing skills and provides personalized course recommendations  
- 📝 Inline resume editing with grammar suggestions  
- 📥 Download AI-enhanced resume and reports

Built using **Python, Streamlit, SentenceTransformers, and Groq LLMs**, this tool blends simplicity with powerful insights to help you become job-ready faster and smarter.

---

Want to get started?  
➡️ Navigate to the **AI Resume Analyzer** tab from the sidebar to upload your resume and begin your journey!
"""

# Render the text
st.markdown(about_text)
col1, col2 = st.columns(2)
with col1:
    if st.button("📝 Analyze your Resume with AI "):
        st.switch_page("pages/1_Resume Analyzer.py")

with col2:
    pass


