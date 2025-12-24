import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. CONFIG ---
st.set_page_config(page_title="Boardroom Brain", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fff; }
    .chat-msg { padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .user-msg { background-color: #2b313e; }
    .bot-msg { background-color: #1e2130; border-left: 5px solid #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("🧠 NEURAL CONFIG")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.divider()
    st.info("Upload a Document (PDF) to activate the Neural Engine.")
    uploaded_file = st.file_uploader("Upload Report/Deck", type=['pdf'])

# --- 3. THE "BRAIN" (PDF PROCESSING) ---
def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_gemini(question, context):
    # --- 1. AUTO-DETECT AVAILABLE MODELS ---
    available_models = []
    # Ask the API: "What models can I actually use?"
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
    
    if not available_models:
        return "❌ Error: Your API Key does not have access to any generation models."

    # --- 2. SELECT THE BEST MODEL ---
    # Priority: Flash (Fast) -> Pro (Smart) -> First available
    model_name = next((m for m in available_models if 'flash' in m), None)
    if not model_name:
        model_name = next((m for m in available_models if 'pro' in m), available_models[0])

    # --- 3. GENERATE ---
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are a high-level Strategic Advisor to a CEO.
    I have given you a document to analyze.
    
    DOCUMENT CONTEXT:
    {context}
    
    USER QUESTION:
    {question}
    
    INSTRUCTIONS:
    - Answer based ONLY on the document provided.
    - Be concise, professional, and insight-driven.
    - If the answer isn't in the doc, say "The document does not cover this."
    """
    
    try:
        response = model.generate_content(prompt)
        return f"**⚡ Utilizing Model:** `{model_name}`\n\n" + response.text
    except Exception as e:
        return f"⚠️ Model Error: {e}"

# --- 4. THE UI ---
st.title("🧠 The Boardroom Brain")
st.caption("Enterprise Document Intelligence System")

# Initialize Session State (Memory)
if "history" not in st.session_state:
    st.session_state.history = []

if uploaded_file and api_key:
    # A. Extract Text
    with st.spinner("Extracting Knowledge Graph..."):
        raw_text = get_pdf_text(uploaded_file)
        st.success(f"Document Indexed: {len(raw_text)} characters loaded.")

    # B. Chat Interface
    query = st.chat_input("Ask a strategic question about this document...")
    
    if query:
        # Add user query to history
        st.session_state.history.append({"role": "user", "text": query})
        
        # Get Answer
        with st.spinner("Analyzing..."):
            answer = ask_gemini(query, raw_text)
            st.session_state.history.append({"role": "bot", "text": answer})

    # C. Display Chat
    for chat in st.session_state.history:
        div_class = "user-msg" if chat["role"] == "user" else "bot-msg"
        st.markdown(f"<div class='chat-msg {div_class}'><strong>{chat['role'].upper()}:</strong> {chat['text']}</div>", unsafe_allow_html=True)

elif not uploaded_file:
    st.markdown("### 🛑 No Data Detected")
    st.markdown("Please upload a PDF (Investor Deck, Contract, or Report) to begin analysis.")
