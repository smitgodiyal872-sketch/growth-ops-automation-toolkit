import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Resume Roaster", page_icon="💀", layout="wide")

# YOUR KEY IS PRE-FILLED HERE
GOOGLE_API_KEY = "AIzaSyBONEgdEtleadyh7g_7jfPSiG-ipn0_btg"

# Setup AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # UPDATED TO YOUR AVAILABLE MODEL 👇
    model = genai.GenerativeModel('gemini-flash-latest')
    status = "🟢 Online (Gemini 2.0)"
except Exception as e:
    status = f"🔴 Offline: {e}"

# --- HELPER FUNCTIONS ---
def get_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except:
        st.error("Could not read PDF. Make sure it's not encrypted.")
    return text

def get_docx_text(uploaded_file):
    try:
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    except:
        st.error("Could not read Word file.")
        return ""

# --- THE UI ---
st.title("💀 The AI Resume Roaster")
st.markdown("### Upload your CV. Let the AI destroy it (for your own good).")
st.caption(f"System Status: {status}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Upload Your Resume")
    uploaded_file = st.file_uploader("Drop your PDF or Docx here:", type=["pdf", "docx"])
    
    resume_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.pdf'):
            resume_text = get_pdf_text(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            resume_text = get_docx_text(uploaded_file)
            
        if resume_text:
            st.success(f"✅ Resume Loaded! ({len(resume_text)} characters)")
            with st.expander("See extracted text"):
                st.write(resume_text)

with col2:
    st.subheader("2️⃣ Paste the Job Description")
    jd_text = st.text_area("Paste the JD here:", height=300)

st.divider()

# --- THE ACTIONS ---
col1, col2, col3 = st.columns(3)

roast_btn = col1.button("🔥 Roast My Resume")
match_btn = col2.button("📊 Check ATS Score")
fix_btn = col3.button("✨ Rewrite My Bullet Points")

# --- THE BRAIN ---
if roast_btn and resume_text:
    with st.spinner("Analyzing your failures..."):
        prompt = f"""
        Act as a brutal hiring manager at a Y Combinator startup. 
        Read this resume:
        {resume_text}

        Roast this candidate. Tell them exactly why you would DELETE this resume. 
        Be mean, be funny, but be honest. Point out vague words, lack of numbers, and fluff.
        """
        try:
            response = model.generate_content(prompt)
            st.error("💀 The Roast:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")

elif match_btn and resume_text and jd_text:
    with st.spinner("Calculating match percentage..."):
        prompt = f"""
        Act as an ATS (Applicant Tracking System).
        Compare this Resume: {resume_text}
        To this Job Description: {jd_text}

        Give a match score out of 100%.
        List 3 keywords missing from the resume.
        """
        try:
            response = model.generate_content(prompt)
            st.info("📊 ATS Report:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")

elif fix_btn and resume_text and jd_text:
    with st.spinner("Fixing your career..."):
        prompt = f"""
        Act as a professional resume writer.
        Take the user's resume: {resume_text}
        And the target JD: {jd_text}

        Rewrite the top 3 bullet points of the resume to include keywords from the JD.
        Use numbers, metrics, and action verbs. Make it sound like a 'Top 1% Operator'.
        """
        try:
            response = model.generate_content(prompt)
            st.success("✨ Improved Bullet Points:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")
