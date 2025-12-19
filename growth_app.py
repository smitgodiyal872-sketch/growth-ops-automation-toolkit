import streamlit as st
import pandas as pd

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Growth Command Center", page_icon="🚀")

# --- 2. THE UI HEADER ---
st.title("🚀 Growth Command Center")
st.write("internal tool to manage leads and automate outreach.")
st.divider()

# --- 3. FILE UPLOADER ---
uploaded_file = st.file_uploader("📂 Upload your Leads CSV", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Show metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Leads", len(df))
    col2.metric("Unique Sources", df['Type'].nunique())
    
    # --- 4. DATA EDITOR ---
    st.subheader("🔍 Lead Database")
    # Interactive table - you can sort and filter inside the browser!
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    # --- 5. EMAIL GENERATOR ---
    st.divider()
    st.subheader("⚡ Automated Outreach Writer")
    
    recipient_name = st.text_input("Enter Recipient Name (for testing)", "Founder")
    service_pitch = st.selectbox("Select Pitch Type", ["Web Design", "SEO Audit", "App Dev"])
    
    if st.button("Generate Cold Email"):
        st.success("Draft Generated!")
        
        # The Email Template Logic
        if service_pitch == "Web Design":
            email_body = f"""
            Subject: Quick question about your website
            
            Hi {recipient_name},
            
            I was researching businesses in Dehradun and found your contact details.
            I noticed your website isn't mobile-optimized, which means you're likely losing 40% of traffic.
            
            I build high-conversion landing pages using Python automation.
            Can I send you a mockup this week?
            
            Best,
            Smit
            """
        else:
            email_body = f"""
            Subject: Scaling your organic traffic
            
            Hi {recipient_name},
            
            Found you in our lead database. Wanted to ask if you are currently looking for help with {service_pitch}?
            
            Best,
            Smit
            """
            
        st.code(email_body, language="text")

else:
    st.info("👆 Upload a CSV file to get started.")

# --- SIDEBAR ---
with st.sidebar:
    st.write("Developed by **Smit Godiyal**")
    st.caption("Day 6 Growth Engineering Project")