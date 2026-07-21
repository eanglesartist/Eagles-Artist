"""
state.py
------------------
Session-level app state: the current user, their credit balance, and
the active Project/Scene being edited. Backed by database/timeline_model.py
dataclasses; persisted to SQLite on save via database/db.py.
"""
import streamlit as st

from database.timeline_model import Project
from database import db

DEFAULT_EMAIL = "demo@eagleartist.ai"


def init_state():
    db.init_databases()

    if "user_email" not in st.session_state:
        st.session_state.user_email = DEFAULT_EMAIL

    if "credits" not in st.session_state:
        st.session_state.credits = db.get_credits(st.session_state.user_email)

    if "projects" not in st.session_state:
        st.session_state.projects = {}

    if "active_project_id" not in st.session_state:
        project = Project(title="Untitled video", owner_email=st.session_state.user_email)
        project.add_scene("attack goat")
        st.session_state.projects[project.id] = project
        st.session_state.active_project_id = project.id

    if "active_scene_id" not in st.session_state:
        active = get_active_project()
        st.session_state.active_scene_id = active.scenes[0].id if active.scenes else None


def get_active_project() -> Project:
    return st.session_state.projects[st.session_state.active_project_id]


def get_active_scene():
    project = get_active_project()
    for scene in project.scenes:
        if scene.id == st.session_state.active_scene_id:
            return scene
    return project.scenes[0] if project.scenes else None


def create_project(title: str = "Untitled video") -> Project:
    project = Project(title=title, owner_email=st.session_state.user_email)
    project.add_scene("new scene")
    st.session_state.projects[project.id] = project
    st.session_state.active_project_id = project.id
    st.session_state.active_scene_id = project.scenes[0].id
    return project


def add_scene_to_active_project(prompt: str = "new scene"):
    project = get_active_project()
    scene = project.add_scene(prompt)
    st.session_state.active_scene_id = scene.id
    return scene
