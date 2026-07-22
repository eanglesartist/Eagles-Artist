import streamlit as st

def init_session_state():
    """Initializes global state variables for the entire studio."""
    defaults = {
        "current_project_id": None,
        "active_tab": "movie_mode",
        "timeline_clips": [],
        "render_queue": [],
        "selected_camera": "ARRI Alexa",
        "is_rendering": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
