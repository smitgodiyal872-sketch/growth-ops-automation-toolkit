import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px

# --- 1. CONFIG ---
st.set_page_config(page_title="Insight Engine", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fff; }
    .chat-box { background-color: #1e2130; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("📊 DATA CONFIG")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.info("Upload a CSV/Excel file. Ask questions. Get Charts.")
    uploaded_file = st.file_uploader("Upload Data", type=['csv', 'xlsx'])

# --- 3. THE BRAIN (CODE GENERATION) ---
def analyze_and_plot(df, query):
    # 1. Get dataset info to give context to AI
    columns = list(df.columns)
    data_sample = df.head(3).to_string()
    
    # 2. Select Model (Auto-detect logic)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = next((m for m in available_models if 'flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)

    # 3. Prompt: "Write Python code to visualize this"
    prompt = f"""
    You are a Python Data Analyst.
    
    DATA CONTEXT:
    Columns: {columns}
    Sample Data:
    {data_sample}
    
    USER REQUEST:
    {query}
    
    TASK:
    Write a snippet of Python code using 'plotly.express' to visualize the answer.
    - Assume the dataframe is already loaded as 'df'.
    - Use 'fig' as the variable for the plot.
    - DO NOT use st.write(). Just create the 'fig' object.
    - If the user asks for a calculation (not a plot), create a variable 'answer' with the string result.
    
    OUTPUT FORMAT:
    Return ONLY the raw Python code. No markdown formatting (no ```python).
    """
    
    response = model.generate_content(prompt)
    return response.text.replace("```python", "").replace("```", "").strip()

# --- 4. THE UI ---
st.title("📊 The Insight Engine")
st.caption("Chat with your data. Visualize instantly.")

if uploaded_file and api_key:
    # A. Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.dataframe(df.head(3), use_container_width=True)
        st.success(f"Loaded {len(df)} rows successfully.")
        
    except Exception as e:
        st.error(f"Error loading file: {e}")

    # B. Chat Interface
    query = st.text_input("Ask a question (e.g., 'Show bar chart of Sales by Region')")
    
    if st.button("🚀 Analyze"):
        with st.spinner("Consulting the AI Analyst..."):
            try:
                # 1. Get the Code from AI
                generated_code = analyze_and_plot(df, query)
                
                # 2. Show the code (Transparency)
                with st.expander("See Generated Python Code"):
                    st.code(generated_code, language='python')
                
                # 3. Execute the Code
                # We define a local dictionary to capture variables created by the exec()
                local_vars = {"df": df, "px": px}
                exec(generated_code, {}, local_vars)
                
                # 4. Display Result
                if 'fig' in local_vars:
                    st.plotly_chart(local_vars['fig'], use_container_width=True)
                elif 'answer' in local_vars:
                    st.info(local_vars['answer'])
                else:
                    st.warning("The AI ran the code but didn't generate a 'fig' or 'answer' variable.")
                    
            except Exception as e:
                st.error(f"Execution Error: {e}")
                st.info("Try rephrasing your prompt to be more specific about the columns.")

elif not uploaded_file:
    st.info("waiting for data...")
