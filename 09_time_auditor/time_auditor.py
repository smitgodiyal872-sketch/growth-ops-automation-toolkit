import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import random

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Exec Ops Auditor", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #0e1117; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .stDataFrame { border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNCTIONS ---
def generate_dummy_data():
    """Generates fake Founder data for the demo."""
    tasks = ['Investor Sync', 'Deep Work: Q3 Strategy', 'Team Standup', 'Lunch with VC', 
             'Code Review', 'Sales Pipeline Review', 'Gym', 'Board Deck Prep', 'Client Call']
    data = []
    
    # Generate 20 fake events
    for i in range(20):
        task = random.choice(tasks)
        day_offset = random.randint(0, 7)
        hour = random.randint(9, 17)
        date = datetime.date.today() + datetime.timedelta(days=day_offset)
        start_time = datetime.datetime.combine(date, datetime.time(hour, 0))
        duration = random.choice([30, 60, 120])
        
        # Categorize Logic
        category = "📂 Admin"
        if "Deep Work" in task or "Code" in task or "Deck" in task: category = "⚡ Deep Work"
        elif "Sync" in task or "Call" in task or "Standup" in task: category = "🗣️ Meetings"
        elif "Gym" in task or "Lunch" in task: category = "🧘 Personal"
        elif "Investor" in task or "VC" in task: category = "💰 Fundraising"

        data.append({"Event": task, "Start": start_time, "Duration (Min)": duration, "Category": category})
    
    return pd.DataFrame(data).sort_values(by="Start")

# --- 3. UI DASHBOARD ---
st.title("⚡ EXECUTIVE TIME AUDITOR")
st.caption("Strategic Time Analysis for High-Performance Teams")

# Sidebar
with st.sidebar:
    st.header("DATA SOURCE")
    data_mode = st.radio("Select Input:", ["🚀 Use Demo Data", "📂 Upload CSV"])
    
    df = None
    if data_mode == "🚀 Use Demo Data":
        if st.button("GENERATE SAMPLE DATA", type="primary"):
            df = generate_dummy_data()
            st.session_state['data'] = df
            st.success("DEMO DATA LOADED")
    else:
        uploaded_file = st.file_uploader("Upload Calendar CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.session_state['data'] = df

# Main Area
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # METRICS
    col1, col2, col3, col4 = st.columns(4)
    total_hours = df['Duration (Min)'].sum() / 60
    deep_work = df[df['Category'] == '⚡ Deep Work']['Duration (Min)'].sum() / 60
    mtg_hours = df[df['Category'] == '🗣️ Meetings']['Duration (Min)'].sum() / 60
    
    col1.metric("Total Hours Logged", f"{total_hours:.1f} hrs")
    col2.metric("Deep Work Ratio", f"{(deep_work/total_hours)*100:.0f}%", "Target: 40%")
    col3.metric("Meeting Load", f"{mtg_hours:.1f} hrs", "-High Risk" if mtg_hours > 10 else "Normal")
    col4.metric("Strategy Score", "B+", "AI Analysis")

    # CHARTS
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("⏳ Where is the time going?")
        fig = px.bar(df, x='Start', y='Duration (Min)', color='Category', 
                     title="Weekly Time Distribution",
                     color_discrete_map={
                         "⚡ Deep Work": "#00FF94", 
                         "🗣️ Meetings": "#FF0055", 
                         "💰 Fundraising": "#FFD700",
                         "🧘 Personal": "#00D4FF",
                         "📂 Admin": "#888888"
                     })
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("🎯 Focus Split")
        fig2 = px.pie(df, names='Category', values='Duration (Min)', hole=0.5,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

    # RAW DATA
    with st.expander("🔎 VIEW RAW CALENDAR DATA"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👈 Select 'Use Demo Data' in the sidebar to see the magic.")
