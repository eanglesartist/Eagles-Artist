"""
styles.py
------------------
Shared CSS injected by every page. Keeps the Google-Flow-style visual
language (canvas, timeline, AI panel, icon rail) consistent app-wide.
"""
import streamlit as st

MOUNTAIN_IMG = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80"

GLOBAL_CSS = """
<style>
    .main .block-container {
        padding-top: 0;
        padding-bottom: 1rem;
        max-width: 100%;
        background-color: #F8FAFC;
    }

    /* ---- Top bar ---- */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 60px;
        padding: 0 20px;
        border-bottom: 1px solid #E2E8F0;
        background: white;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .logo-area { display: flex; align-items: center; gap: 10px; }
    .logo-badge {
        width: 32px; height: 32px; border-radius: 8px;
        background: linear-gradient(135deg, #6366F1, #A855F7);
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 15px;
    }
    .title-block {
        display: flex; align-items: center; gap: 8px;
        font-weight: 700; font-size: 15px; color: #1E293B;
    }
    .menu {
        display: flex; gap: 16px; font-size: 13px; color: #475569;
        font-weight: 500; margin-left: 24px;
    }
    .top-actions { display: flex; align-items: center; gap: 12px; }
    .credits-pill {
        background: #FEF3C7; color: #92400E; font-weight: 700;
        font-size: 12px; padding: 6px 12px; border-radius: 20px;
    }
    .top-link {
        font-size: 13px; color: #475569; font-weight: 500; cursor: pointer;
    }
    .btn-play-outline {
        background: white; color: #1E293B; border: 1px solid #CBD5E1;
        border-radius: 20px; padding: 6px 18px; font-weight: 600;
        font-size: 13px; cursor: pointer;
    }
    .btn-share-solid {
        background: #3B82F6; color: white; border: none;
        padding: 6px 16px; border-radius: 20px; font-weight: 600;
        font-size: 13px; cursor: pointer;
    }
    .avatar-circle {
        width: 32px; height: 32px; border-radius: 50%;
        background: linear-gradient(135deg, #FBBF24, #F97316);
        display: flex; align-items: center; justify-content: center; font-size: 14px;
    }

    /* ---- Canvas ---- */
    .canvas-box {
        background: white; border: 1px solid #E2E8F0; border-radius: 4px;
        height: 440px; position: relative; overflow: hidden; margin-bottom: 8px;
    }
    .canvas-image {
        width: 100%; height: 100%;
        background: url('MOUNTAIN_IMG_URL') center/cover; position: relative;
    }
    .time-chip {
        position: absolute; bottom: 10px; right: 12px;
        background: rgba(0,0,0,0.6); color: white; padding: 2px 8px;
        border-radius: 4px; font-size: 11px; font-weight: 500;
    }

    /* ---- Timeline ---- */
    .timeline-box {
        background: #F8FAFC; border-radius: 12px;
        padding: 12px 20px 18px 20px; display: flex; flex-direction: column; gap: 12px;
    }
    .timeline-controls {
        display: flex; justify-content: space-between; align-items: center;
        font-size: 13px; color: #475569;
    }
    .timeline-track { display: flex; align-items: center; gap: 10px; overflow-x: auto; }
    .clip-thumbnail {
        min-width: 170px; height: 70px; border: 2px solid #3B82F6; border-radius: 8px;
        background: linear-gradient(90deg, rgba(59,130,246,0.85), rgba(29,78,216,0.85)),
                    url('MOUNTAIN_IMG_URL') center/cover;
        display: flex; align-items: flex-end; padding: 6px; color: white;
        font-size: 11px; font-weight: 600; position: relative;
    }
    .clip-thumbnail.active { outline: 2px solid #1D4ED8; outline-offset: 2px; }
    .add-clip-btn {
        width: 36px; height: 36px; border-radius: 50%; background: #EFF6FF;
        color: #3B82F6; border: none; font-size: 18px; font-weight: bold;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }

    /* ---- AI panel ---- */
    .ai-panel-header {
        display: flex; align-items: center; gap: 8px; font-weight: 700;
        font-size: 15px; color: #1E293B; margin-bottom: 6px;
    }
    .expanded-prompt-box {
        background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px;
        padding: 10px 12px; font-size: 12.5px; color: #075985; line-height: 1.5;
    }

    /* ---- Icon sidebar ---- */
    .icon-sidebar {
        background: white; border-left: 1px solid #E2E8F0;
        display: flex; flex-direction: column; align-items: center;
        padding-top: 18px; gap: 18px;
    }
    .icon-nav-item {
        display: flex; flex-direction: column; align-items: center; gap: 4px;
        font-size: 10px; color: #475569; font-weight: 500;
    }
    .icon-nav-item .glyph { font-size: 18px; }
    .icon-nav-item.active { color: #3B82F6; }

    /* ---- Dashboard cards ---- */
    .dash-card {
        background: white; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 18px; text-align: center;
    }
    .dash-card h3 { margin: 6px 0 2px 0; font-size: 15px; }
    .dash-card p { margin: 0; font-size: 12px; color: #64748B; }
</style>
""".replace("MOUNTAIN_IMG_URL", MOUNTAIN_IMG)


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
