import streamlit as st
import uuid

def init_session_state():
    """Initialize all Streamlit session state variables."""
    if "user_credits" not in st.session_state:
        st.session_state["user_credits"] = 1250
    if "current_video" not in st.session_state:
        st.session_state["current_video"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = str(uuid.uuid4())
    if "_db_synced" not in st.session_state:
        st.session_state["_db_synced"] = True
