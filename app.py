import streamlit as st
import os

# Ensure necessary directories exist locally
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.set_page_config(
    page_title="AI Cinematic Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Placeholder for your main UI components
st.title("🎬 AI Cinematic Studio")
st.write("Workspace initialized successfully.")
