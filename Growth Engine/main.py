import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="Growth Ops Engine", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fff; }
    .stTextArea textarea { background-color: #1e2130; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (API KEY) ---
with st.sidebar:
    st.header("⚙️ ENGINE ROOM")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    tone = st.selectbox("Select Tone", ["Founders Mode (Punchy)", "Educational (How-To)", "Storytelling (Vulnerable)"])
    if api_key:
        genai.configure(api_key=api_key)

# --- 3. THE PROMPTS ---
def generate_content(topic, raw_text, tone):
    # 1. AUTO-DETECT AVAILABLE MODELS
    # This asks your API key: "What models can I use?"
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
    
    # 2. SELECT THE BEST ONE
    # Tries to find 'flash' (fastest), then 'pro', then defaults to the first one found.
    if not available_models:
        return "Error: Your API Key has no access to generation models."
        
    model_name = next((m for m in available_models if 'flash' in m), None)
    if not model_name:
        model_name = next((m for m in available_models if 'pro' in m), available_models[0])
    
    # 3. GENERATE
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are a viral ghostwriter for a Tech Founder. 
    Tone: {tone}
    Topic: {topic}
    Raw Input: {raw_text}

    TASK:
    1. Write a **LinkedIn Post**:
       - Hook: Short, punchy, pattern-interrupt.
       - Body: Scannable, use bullet points, "Value per line" philosophy.
       - CTA: Ask a question or point to a link.
    
    2. Write a **Twitter/X Thread** (3 tweets max):
       - Tweet 1: The Hook.
       - Tweet 2: The Insight/How-to.
       - Tweet 3: The takeaway.
    """
    
    response = model.generate_content(prompt)
    return f"**Using Model:** `{model_name}`\n\n" + response.text

# --- 4. UI DASHBOARD ---
st.title("🚀 CONTENT OPS ENGINE")
st.caption("Turn raw thoughts into distribution assets instantly.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 RAW INPUT")
    topic = st.text_input("Topic (e.g., 'I built a time auditor')")
    raw_text = st.text_area("Paste code, notes, or rant here:", height=300)
    
    generate_btn = st.button("⚡ IGNITE ENGINE", type="primary")

with col2:
    st.subheader("📤 DISTRIBUTION ASSETS")
    if generate_btn and api_key and raw_text:
        with st.spinner("Refining hooks..."):
            try:
                result = generate_content(topic, raw_text, tone)
                st.markdown(result)
                st.success("Assets Generated.")
            except Exception as e:
                st.error(f"Error: {e}")
    elif generate_btn and not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar.")
    else:
        st.info("Awaiting Input...")
