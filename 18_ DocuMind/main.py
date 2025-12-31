import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. CONFIG ---
st.set_page_config(page_title="DocuMind", page_icon="📄", layout="centered")

# Custom CSS for chat
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    .chat-msg { padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .user-msg { background-color: #e6f3ff; border-left: 5px solid #007ACC; }
    .ai-msg { background-color: #f0f2f6; border-left: 5px solid #00d26a; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("📄 DOCUMIND")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.info("Upload a PDF. Chat with it.")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

# --- 3. SESSION STATE (Memory) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# --- 4. LOGIC (Extract & Generate) ---
def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_gemini(query, context):
    # --- AUTO-DETECT MODEL FIX ---
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Priority: Flash -> Pro -> First Available
    model_name = next((m for m in available_models if 'flash' in m), None)
    if not model_name:
        model_name = next((m for m in available_models if 'pro' in m), available_models[0])
    
    model = genai.GenerativeModel(model_name)
    # -----------------------------
    
    prompt = f"""
    You are a helpful Research Assistant. Answer the question based ONLY on the document provided.
    
    DOCUMENT CONTEXT:
    {context[:30000]} # Limit context to save tokens
    
    USER QUESTION:
    {query}
    
    Answer clearly and concisely.
    """
    response = model.generate_content(prompt)
    return response.text

# --- 5. UI ---
st.title("📄 DocuMind: Chat with PDF")

if uploaded_file:
    # A. Process PDF (Only once)
    if st.session_state.pdf_text == "":
        with st.spinner("Reading document..."):
            st.session_state.pdf_text = get_pdf_text(uploaded_file)
            st.success("Document loaded! Ask me anything.")

    # B. Chat History Display
    for role, message in st.session_state.chat_history:
        css_class = "user-msg" if role == "User" else "ai-msg"
        st.markdown(f"<div class='chat-msg {css_class}'><strong>{role}:</strong> {message}</div>", unsafe_allow_html=True)

    # C. Input Area
    user_query = st.chat_input("Ask about the document...")
    
    if user_query and api_key:
        # 1. Append User Msg
        st.session_state.chat_history.append(("User", user_query))
        
        # 2. Get Answer
        with st.spinner("Thinking..."):
            answer = ask_gemini(user_query, st.session_state.pdf_text)
        
        # 3. Append AI Msg
        st.session_state.chat_history.append(("AI", answer))
        
        # 4. Refresh to show new message
        st.rerun()

elif not uploaded_file:
    st.info("Waiting for PDF upload...")
