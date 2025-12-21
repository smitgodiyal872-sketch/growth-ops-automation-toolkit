import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
from pypdf import PdfReader
from docx import Document

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Job Hunt HQ", page_icon="⚡", layout="wide")

# FIX: DIRECT KEY FOR LOCAL USE (No Secrets Error)
# GOOGLE_API_KEY = "PASTE_YOUR_KEY_HERE"
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Default DNA
DEFAULT_DNA = """WHO AM I:
I am a "Technical Operator." 
I am not just a marketer; I can code (Python, Java, Spring Boot).
I am not just a coder; I understand Growth, Revenue, and Content.
I edit videos in Adobe Premiere Pro daily.
I build my own tools (like this Streamlit app) to solve problems.
I don't wait for instructions. I figure it out.

MY VOICE (FOUNDER MODE):
- Short sentences.
- No "I hope this finds you well."
- No "I am writing to apply."
- Use numbers and specific tools.
- Confident, but not arrogant.
- Focus on "What I can build for you tomorrow."
"""

# Setup AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest') 
    status_text = "SYSTEM ONLINE"
    status_color = "#00FF94" 
except Exception as e:
    status_text = "SYSTEM OFFLINE"
    status_color = "#FF0055" 

# --- 2. CYBERPUNK STYLING ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');
    .stApp {{ background-color: #0e1117; color: #e0e0e0; font-family: 'Inter', sans-serif; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{ background-color: #0e1117; border-right: 1px solid rgba(255,255,255,0.1); }}
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.05) !important; color: #e0e0e0 !important;
        border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 8px;
    }}
    .watermark {{
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(14,17,23,0.8); border: 1px solid rgba(255,255,255,0.1);
        padding: 8px 16px; border-radius: 30px; color: #00FF94;
        font-family: 'JetBrains Mono', monospace; font-size: 11px; pointer-events: none;
    }}
    </style>
    <div class="watermark">⚡ ARCHITECTED BY SMIT GODIYAL</div>
""", unsafe_allow_html=True)

# --- 3. FUNCTIONS ---
def get_pdf_text(uploaded_file):
    try: return "".join([page.extract_text() for page in PdfReader(uploaded_file).pages])
    except: return ""

def get_docx_text(uploaded_file):
    try: return "\n".join([para.text for para in Document(uploaded_file).paragraphs])
    except: return ""

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2921/2921222.png", width=60)
    st.markdown("## OPERATOR HQ")
    st.markdown(f'<span style="color:{status_color}">● {status_text}</span>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("RESUME", type=["pdf", "docx"], label_visibility="collapsed")
    resume_text = ""
    if uploaded_file:
        if uploaded_file.name.endswith('.pdf'): resume_text = get_pdf_text(uploaded_file)
        elif uploaded_file.name.endswith('.docx'): resume_text = get_docx_text(uploaded_file)
        st.success(f"LOCKED: {uploaded_file.name}")

    jd_text = st.text_area("JOB DESCRIPTION", height=150, placeholder="Paste JD here...", label_visibility="collapsed")
    dna_context = st.text_area("OPERATOR DNA", value=DEFAULT_DNA, height=200, label_visibility="collapsed")

# --- 5. MAIN APP ---
st.title("JOB HUNT COMMAND CENTER")
tab1, tab2 = st.tabs(["🔥 ROAST", "✉️ STRATEGIC OUTREACH"])

with tab1:
    if st.button("🔥 ROAST RESUME", use_container_width=True):
        if resume_text:
            prompt = f"Act as a brutal YC Founder. Roast this resume: {resume_text}. Be mean."
            st.markdown(model.generate_content(prompt).text)
    
    if st.button("✨ OPTIMIZE BULLETS", use_container_width=True):
        if resume_text and jd_text:
            prompt = f"Rewrite top 3 bullets of: {resume_text} for JD: {jd_text}. Use numbers. Context: {dna_context}"
            st.markdown(model.generate_content(prompt).text)

with tab2:
    st.subheader("🚀 TARGET LIST SEGMENTATION")
    
    # 1. Initialize Table
    if 'targets' not in st.session_state:
        st.session_state.targets = pd.DataFrame([
            {"Name": "Sam Altman", "Company": "OpenAI", "Role": "CEO", "Strategy": "Founder Mode (Direct)"},
            {"Name": "Recruiter Name", "Company": "OpenAI", "Role": "Talent Lead", "Strategy": "Recruiter Friendly (Keywords)"}
        ])

    # 2. UPGRADED STRATEGY LIST
    strategy_options = [
        "Founder Mode (Direct & Short)",           # For CEOs/Founders
        "Value First (Technical/Builder)",         # For CTOs/Engineers
        "The Audit (I found a bug/fix)",           # High Risk/High Reward
        "Recruiter Friendly (Professional)",       # For HR/Talent Acquisition
        "The ROI Pitch (Money/Growth)",            # For Sales/Marketing Heads
        "The Fanboy (Passionate User)",            # For Product Managers
        "The Networker (Warm/Polite)"              # For Alumni/Connections
    ]

    # 3. Editable Grid
    edited_df = st.data_editor(
        st.session_state.targets, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Strategy": st.column_config.SelectboxColumn(
                "Strategy",
                width="medium",
                options=strategy_options,
                required=True
            )
        }
    )

    if st.button("⚡ EXECUTE BATCH", type="primary", use_container_width=True):
        if resume_text and jd_text:
            progress = st.progress(0)
            for i, row in edited_df.iterrows():
                progress.progress((i + 1) / len(edited_df))
                
                current_strategy = row['Strategy']
                
                # --- INTELLIGENT PROMPT ---
                prompt = f"""
                Write a cold email to {row['Name']} ({row.get('Role', 'Lead')}) at {row['Company']}.
                
                **MY DNA (CONTEXT):** {dna_context}
                **MY RESUME:** {resume_text}
                **THE JOB:** {jd_text}
                
                **SELECTED STRATEGY: {current_strategy}**
                
                **STRATEGY RULES:**
                - If "Founder Mode": Be extremely short. No fluff. Value only.
                - If "The Audit": Mention a specific hypothetical improvement or fix relevant to their company.
                - If "Recruiter Friendly": Use keywords from the JD. Be polite and professional.
                - If "The ROI Pitch": Focus entirely on revenue, growth, and numbers.
                
                **GENERAL RULES:**
                1. Subject line must be lower-case and catchy.
                2. Max 100 words.
                3. First line must hook them immediately.
                4. Sign off with the name found in the 'MY DNA' section.
                """
                
                try:
                    res = model.generate_content(prompt)
                    with st.expander(f"✉️ {row['Name']} ({current_strategy})", expanded=True):
                        st.code(res.text, language="text")
                    time.sleep(2) # Prevent Rate Limits
                except Exception as e:
                    st.error(f"Failed for {row['Name']}: {e}")
            
            st.success("BATCH COMPLETE")
            progress.empty()
        else:
            st.error("UPLOAD RESUME & JD FIRST")
