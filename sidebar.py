"""
sidebar.py
------------------
Far-right tool icon rail.
"""
import streamlit as st

ICON_ITEMS = [
    ("ai_video", "🎬", "AI Video"),
    ("avatar", "👤", "Avatar"),
    ("voiceover", "🎙️", "Voiceover"),
    ("image", "🖼️", "Image"),
    ("record", "⏺️", "Record"),
    ("uploads", "📁", "Uploads"),
    ("stock", "📈", "Stock"),
    ("captions", "💬", "Captions"),
    ("text", "T", "Text"),
    ("templates", "🗂️", "Templates"),
    ("shapes", "⭐", "Shapes"),
]


def render_icon_sidebar(active: str = "ai_video"):
    items_html = ""
    for key, glyph, label in ICON_ITEMS:
        cls = "icon-nav-item active" if key == active else "icon-nav-item"
        items_html += f'<div class="{cls}"><span class="glyph">{glyph}</span><span>{label}</span></div>'

    st.markdown(f'<div class="icon-sidebar">{items_html}</div>', unsafe_allow_html=True)
