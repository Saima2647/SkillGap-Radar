import streamlit as st  # used for frontend buttons, input fields, layout, etc.
from pdfminer.high_level import extract_text # extract text from pdf
from sentence_transformers import SentenceTransformer # generate Embeddings of text like vector A, vector B
from sklearn.metrics.pairwise import cosine_similarity # helps in calculating the score from the vector 
from groq import Groq # API for genrating ai report
import re # regular expression function extract pattens from the text 
from dotenv import load_dotenv # extract API Key from .env file
import os # used to intract with environment to extract API  
import urllib.parse as ul # used to manuplate url
import tempfile # create a temporary file for pdf
import base64 # converts file into binary for downloading and putting html buttons 
from fpdf import FPDF # genrate pdf


load_dotenv() # load environment
api_key = os.getenv("GROQ_API_KEY") # fetch API key

#This block makes sure that these variables exist in Streamlit memory before we use them, 
#so we can avoid errors and keep user inputs saved across interactions.

for key in ["form_submitted", "resume", "job_desc"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# title
st.title("AI Resume Analyzer 📝")

# <------- Defining Functions ------->

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    try:
        extracted_text = extract_text(uploaded_file)
        return extracted_text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return "Could not extract text from the PDF file."

# Function to calculate similarity 
#Convert both texts into numerical vectors using BERT, These vectors represent the meaning of the texts in mathematical terms.
def calculate_similarity_bert(text1, text2):
    ats_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')      
    # Encode the texts directly to embeddings
    embeddings1 = ats_model.encode([text1])
    embeddings2 = ats_model.encode([text2])
    
    # Calculate cosine similarity without adding an extra list layer
    #Resume text	→ SentenceTransformer	→ Embedding Vector A
    #Job description	→ SentenceTransformer	→ Embedding Vector B
    #A & B → cosine_similarity	→ Score (0.0–1.0)	e.g. 0.83
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return similarity

# sends resume and jd to the ai to genrate the report 
def get_report(resume,job_desc):
    client = Groq(api_key=api_key)

    prompt=f"""
    # Context:
    - You are an AI Resume Analyzer, you will be given Candidate's resume and Job Description of the role he is applying for.

    # Instruction:
    - Analyze candidate's resume based on the possible points that can be extracted from job description,and give your evaluation on each point with the criteria below:  
    - Consider all points like required skills, experience,etc that are needed for the job role.
    - Calculate the score to be given (out of 5) for every point based on evaluation at the beginning of each point with a detailed explanation.  
    - If the resume aligns with the job description point, mark it with ✅ and provide a detailed explanation.  
    - If the resume doesn't align with the job description point, mark it with ❌ and provide a reason for it.  
    - If a clear conclusion cannot be made, use a ⚠️ sign with a reason. 
    - After the evaluation, **create a section named "Missing Skills List"**. 
    - In "Missing Skills List", **list 3-5 key technical or domain skills** that are present in the job description but missing from the resume.
    - The Final Heading should be "Suggestions to improve your resume:" and give where and what the candidate can improve to be selected for that job role.

    # Inputs:
    Candidate Resume: {resume}
    ---
    Job Description: {job_desc}

    # Output:
    - Each any every point should be given a score (example: 3/5 ). 
    - Mention the scores and  relevant emoji at the beginning of each point and then explain the reason.
    - A separate section at the end titled **Missing Skills List:** with bullet points or JSON list bullet points cam be emojies.
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# used to extract score from ai generated report to calculate average, calculate the average AI rating
def extract_scores(text):
    # Regular expression pattern to find scores in the format x/5, where x can be an integer or a float
    pattern = r'(\d+(?:\.\d+)?)/5'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    # Convert matches to floats
    scores = [float(match) for match in matches]
    return scores

def extract_missing_skills_from_ai_section(report: str):
    match = re.search(r"Missing Skills List\s*:\s*(.+?)Suggestions to improve", report, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(1).strip()
        lines = [line.strip("–-•*🔸•➡️ ").strip() for line in section.strip().splitlines()]
        skills = [line for line in lines if line and not line.lower().startswith("suggestions")]
        return skills[:5]
    return []

# <--------- Starting the Work Flow ---------> 

# displays form only if the form is not submitted
if not st.session_state.form_submitted:
    with st.form("my_form"):

        # Taking input a Resume (PDF) file 
        resume_file = st.file_uploader(label="Upload your Resume/CV in PDF format", type="pdf")

        # Taking input Job Description
        st.session_state.job_desc = st.text_area("Enter the Job Description of the role you are applying for:",placeholder="Job Description...")

        # Form Submission Button
        submitted = st.form_submit_button("Analyze")
        if submitted:

            #  Allow only if Both Resume and Job Description are Submitted
            if st.session_state.job_desc and resume_file:
                st.info("Extracting Information")

                st.session_state.resume = extract_pdf_text(resume_file) # calling the function to extract text from Resume

                st.session_state.form_submitted = True
                st.rerun()                 # refresh the page to close the form and give results

            # Do not allow if not uploaded
            else:
                st.warning("Please Upload both Resume and Job Description to analyze")


if st.session_state.form_submitted:
    score_place = st.info("Generating Scores...")

    # Call the function to get ATS Score
    ats_score = calculate_similarity_bert(st.session_state.resume,st.session_state.job_desc)

    col1,col2 = st.columns(2,border=True)
    with col1:
        st.write("Few ATS uses this score to shortlist candidates, Similarity Score:")
        st.subheader(str(ats_score))

    # Call the function to get the Analysis Report from LLM (Groq)
    report = get_report(st.session_state.resume,st.session_state.job_desc)
    missing_skills = extract_missing_skills_from_ai_section(report)

    # Calculate the Average Score from the LLM Report
    report_scores = extract_scores(report)                 # Example : [3/5, 4/5, 5/5,...]
    avg_score = sum(report_scores) / (5*len(report_scores))  # Example: 2.4


    with col2:
        st.write("Total Average score according to our AI report:")
        st.subheader(str(avg_score))
    score_place.success("Scores generated successfully!")
    
    st.subheader("AI Generated Analysis Report:")

    # Displaying Report 
    st.markdown(f"""
            <div style='text-align: left; background-color: white; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                {report}
            </div>
            """, unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)

    with col1:

        # Button: View Course Recommendations
        if missing_skills:
            if st.button("📚 View Course Recommendations"):
                st.session_state["skills"] = missing_skills
                st.switch_page("pages/2_View Course Recommendations.py")
        else:
            st.info("✅ No missing skills detected compared to the Job Description.")

         # Download Button
        st.download_button(label="Download Report",data=report,file_name="report.txt")
    with col2:

        # Button: Builded Resume
        if missing_skills and st.button("🤖 Edit Resume with AI"):
            st.session_state.resume_text = st.session_state.resume
            st.session_state.skills = missing_skills
            st.switch_page("pages/3_Edit Resume with AI.py")

        # Button: Build Resume
        if st.button("🛠 Edit Resume with Docs"):
            st.session_state.skills = missing_skills
            st.session_state.resume_text = st.session_state.resume
            st.switch_page("pages/4_Edit Resume with Docs.py")


    


# <-------------- End of the Work Flow --------------->
