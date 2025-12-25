import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIG ---
st.set_page_config(page_title="Voice Ops Agent", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fff; }
    .data-card { background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #00d26a; margin-bottom: 20px; }
    .email-card { background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("🎙️ VOICE OPS")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.info("Record a voice note about a meeting. The AI will structure it and draft a follow-up.")

# --- 3. THE BRAIN (AUDIO PROCESSING) ---
def process_audio(audio_file):
    # 1. AUTO-DETECT AVAILABLE MODELS
    # We ask the API key what it is allowed to use
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            
    if not available_models:
        return '{"error": "No models found"}'

    # 2. SELECT BEST MODEL (Flash is best for audio, but we fallback if needed)
    model_name = next((m for m in available_models if 'flash' in m), None)
    if not model_name:
        model_name = next((m for m in available_models if 'pro' in m), available_models[0])

    # 3. GENERATE
    model = genai.GenerativeModel(model_name)
    
    prompt = """
    You are a Chief of Staff. Listen to this voice note.
    
    TASK 1: Extract structured data JSON:
    - Name
    - Company
    - Role
    - Context/Meeting Notes
    - Action Items
    
    TASK 2: Write a Follow-Up Email:
    - Tone: Professional but casual.
    - Mention specific details.
    
    OUTPUT FORMAT:
    {
        "crm_data": { ...JSON fields... },
        "email_draft": "...email text..."
    }
    Return ONLY valid JSON. Do not use Markdown formatting like ```json.
    """
    
    response = model.generate_content([prompt, {"mime_type": "audio/wav", "data": audio_file.getvalue()}])
    return response.text
    
    # Pass the audio bytes directly to Gemini
    response = model.generate_content([prompt, {"mime_type": "audio/wav", "data": audio_file.getvalue()}])
    return response.text

# --- 4. THE UI ---
st.title("🎙️ Voice-to-CRM Agent")
st.caption("Don't type. Just talk. AI handles the admin.")

# The Audio Recorder Widget
audio_value = st.audio_input("Record your meeting notes")

if audio_value and api_key:
    with st.spinner("🎧 Listening and processing..."):
        try:
            # Get raw text response
            raw_response = process_audio(audio_value)
            
            # Clean up JSON (remove markdown ticks if present)
            clean_json = raw_response.replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            
            crm = data['crm_data']
            email = data['email_draft']
            
            # DISPLAY: CRM Card
            st.subheader("📂 Structured CRM Entry")
            st.markdown(f"""
            <div class='data-card'>
                <h3>👤 {crm.get('Name', 'Unknown')}</h3>
                <p><strong>🏢 Company:</strong> {crm.get('Company', 'N/A')}</p>
                <p><strong>💼 Role:</strong> {crm.get('Role', 'N/A')}</p>
                <p><strong>📝 Notes:</strong> {crm.get('Context/Meeting Notes', '-')}</p>
                <p><strong>⚡ Action Items:</strong> {crm.get('Action Items', '-')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # DISPLAY: Email Card
            st.subheader("✉️ Auto-Drafted Follow-Up")
            st.markdown(f"<div class='email-card'>{email}</div>", unsafe_allow_html=True)
            
            # Copy Button (Text Area for easy copying)
            st.text_area("Copy Email:", value=email, height=200)

        except Exception as e:
            st.error(f"Error: {e}")
            st.expander("See Raw Output").write(raw_response if 'raw_response' in locals() else "No response")

elif audio_value and not api_key:
    st.warning("⚠️ Enter API Key in sidebar first.")
