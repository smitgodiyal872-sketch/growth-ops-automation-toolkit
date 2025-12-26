import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. CONFIG ---
st.set_page_config(page_title="Resume Architect", page_icon="👔", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fff; }
    .score-card { background-color: #1e2130; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #4b5563; }
    .fix-card { background-color: #161b22; padding: 15px; border-radius: 10px; border-left: 5px solid #00d26a; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("👔 ARCHITECT CONFIG")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.info("Upload your 'Master Resume' and paste the Job Description. AI will tailor your application.")

# --- 3. THE BRAIN ---
def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, jd_text):
    # Auto-detect model
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = next((m for m in available_models if 'flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    You are an expert ATS (Applicant Tracking System) and Career Coach.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION (JD):
    {jd_text}
    
    TASK:
    1. **Match Score**: Give a strict score (0-100%) on how well the resume fits the JD.
    2. **Missing Keywords**: List the top 3-5 hard skills/tools in the JD that are missing from the resume.
    3. **Tailored Summary**: WRITE a new "Professional Summary" (3-4 lines) for this candidate that specifically targets this JD. Use the missing keywords naturally.
    4. **Bullet Point Remix**: Choose 2 existing bullet points from the resume and REWRITE them to sound more like the JD (using "Action-Result" format).

    OUTPUT FORMAT (Markdown):
    ## 📊 Match Score: [Score]%
    
    ### 🛑 Missing Keywords
    * [Keyword 1]
    * [Keyword 2]
    
    ### 📝 Tailored Summary (Copy-Paste this)
    > [New Summary]
    
    ### ⚡ Bullet Point Remix
    **Original:** [Idea of old bullet]
    **🚀 New Version:** [Rewritten bullet]
    
    **Original:** [Idea of old bullet]
    **🚀 New Version:** [Rewritten bullet]
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- 4. THE UI ---
st.title("👔 Resume Architect")
st.caption("Stop sending generic resumes. Tailor them in seconds.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Inputs")
    uploaded_resume = st.file_uploader("Upload Master Resume (PDF)", type=['pdf'])
    jd_text = st.text_area("Paste Job Description Here", height=300)
    
    analyze_btn = st.button("🚀 ARCHITECT MY RESUME", type="primary")

with col2:
    st.subheader("📤 Tailored Output")
    if analyze_btn and api_key and uploaded_resume and jd_text:
        with st.spinner("Analyzing keywords & gaps..."):
            try:
                # 1. Extract Text
                resume_text = get_pdf_text(uploaded_resume)
                
                # 2. Analyze
                result = analyze_resume(resume_text, jd_text)
                
                # 3. Render
                st.markdown(result)
                st.success("Optimization Complete.")
                
            except Exception as e:
                st.error(f"Error: {e}")
    elif analyze_btn and not api_key:
        st.warning("⚠️ Enter API Key in sidebar.")
    elif analyze_btn:
        st.info("⚠️ Please upload a resume and paste a JD.")
