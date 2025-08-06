# 🎯 SkillGap Radar – AI-Powered Resume Analyzer

SkillGap Radar is an intelligent, AI-powered web application that analyzes resumes against job descriptions to identify missing skills, recommend personalized learning paths, and enhance resumes using natural language processing (NLP) and generative AI models.

---

## 📌 Features

✅ Upload your resume (PDF) and a job description   
✅ NLP-based analysis and skill matching  
✅ AI-generated evaluation report with improvement suggestions  
✅ Detection of missing technical/domain-specific skills  
✅ Course recommendations from YouTube based on gaps  
✅ Inline editing of resumes with grammar fixes  
✅ Google Docs integration for cloud-based resume updates  
✅ Download AI-enhanced and manually edited resumes as PDFs  

---

## 🚀 How It Works

1. Upload your resume (PDF format).
2. Paste a job description you’re targeting.
3. Get:
   - ATS Score
   - AI-based resume review
   - Missing skill list
   - Personalized course suggestions
4. Edit your resume with AI or Google Docs.
5. Download updated resume and share confidently.

---

## 🧠 Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core backend logic |
| **Streamlit** | Frontend web framework |
| **spaCy & NLTK** | NLP resume parsing |
| **SentenceTransformers** | Semantic similarity analysis |
| **Groq (LLM API)** | AI-powered suggestions |
| **FPDF** | Resume PDF generation |
| **YouTube Data API v3** | Course recommendations |
| **Google Docs & Drive API** | Resume editing in cloud |
| **dotenv** | Secure API key management |

---

## 📂 Folder Structure
SkillGap-Radar/ <br>
├── .env # API keys <br>
├── Home.py # Project landing page <br>
├── pages/ <br>
│ ├── 1_Resume Analyzer.py # Resume + JD upload & analysis <br>
│ ├── 2_View Course Recommendations.py # YouTube course suggestions <br>
│ ├── 3_Edit Resume with AI.py # AI inline resume editor <br>
│ └── 4_Edit Resume with Docs.py # Edit resume using Google Docs <br>
├── utils/ <br>
│ └── css.py # Custom button styling <br>
├── credentials/ # Google OAuth secret & token <br>
│ ├── client_xxx.json <br>
│ └── token.json <br>
└── README.md <br>

---

## 🛡️ Prerequisites

- Python 3.9+
- Google Cloud Project with Docs & Drive API enabled
- `.env` file with:
  - GROQ_API_KEY=your_key
  - YOUTUBE_API_KEY=your_key

---

## ⚙️ Installation

**1. Clone the repo**
git clone https://github.com/Saima2647/skillgap-radar.git
cd skillgap-radar

**2. Create a virtual environment**
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

**3. Install requirements**
pip install -r requirements.txt

**4. Run the app**
streamlit run Home.py

---

## 🔑 API Keys Required
- Groq → For AI evaluation suggestions
- YouTube Data API v3 → For skill-based course videos
- Google Docs & Drive API → For document creation and editing
- All credentials stored securely in .env and credentials/ folder

---

## 📸 Screenshots

**1. Home Page**
   <img width="959" height="503" alt="home resume" src="https://github.com/user-attachments/assets/2b6c06e5-868f-4747-81e4-f8a9264a26b7" />

**2. Resume Analyzer**
   <img width="959" height="503" alt="resume form" src="https://github.com/user-attachments/assets/9bade78e-d0dc-477c-8d8b-d2863f42ac39" />
<img width="959" height="503" alt="resume report" src="https://github.com/user-attachments/assets/d64846e2-d9d6-41ae-a736-714da4ee8a94" />

**3 Skill Gap to Course Recommendation**
<img width="959" height="503" alt="view recomendation" src="https://github.com/user-attachments/assets/a87e7ba5-ee86-4f96-aab4-136ef1018d49" />

**4 Resume Builder & Editor**
Offers two editing options:
  **a. AI-generated improved resume**
  <img width="959" height="504" alt="edit resume ai" src="https://github.com/user-attachments/assets/11903080-ad1e-4456-965b-e39673af3beb" />

  **b. Edit using Google Docs integration**
  <img width="959" height="503" alt="edit with doc" src="https://github.com/user-attachments/assets/23630a84-1333-400d-a6b2-f0b926374dd5" />
  <img width="959" height="503" alt="edit docs" src="https://github.com/user-attachments/assets/89d1f776-487c-4b10-8783-f4e5c9ad598e" />











