import streamlit as st

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="AI Video Editor Workspace",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MOUNTAIN_IMG = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80"

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown(
    """
<style>
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
        background-color: #F8FAFC;
    }

    /* Top bar */
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
    .logo-area {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .logo-badge {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        background: linear-gradient(135deg, #6366F1, #A855F7);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 13px;
    }
    .title-block {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        font-size: 15px;
        color: #1E293B;
    }
    .title-icon {
        font-size: 13px;
        color: #94A3B8;
        cursor: pointer;
    }
    .menu {
        display: flex;
        gap: 18px;
        font-size: 13px;
        color: #475569;
        font-weight: 500;
        margin-left: 26px;
    }
    .top-actions {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .icon-btn {
        font-size: 16px;
        color: #64748B;
        cursor: pointer;
    }
    .btn-play-outline {
        background: white;
        color: #1E293B;
        border: 1px solid #CBD5E1;
        border-radius: 20px;
        padding: 6px 18px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
    }
    .btn-share-solid {
        background: #3B82F6;
        color: white;
        border: none;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
    }
    .avatar-circle {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FBBF24, #F97316);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }

    /* Secondary Toolbar */
    .sub-toolbar {
        background: white;
        border-bottom: 1px solid #E2E8F0;
        padding: 6px 16px;
        display: flex;
        gap: 4px;
        font-size: 14px;
        color: #64748B;
        align-items: center;
        height: 44px;
    }
    .tool-icon {
        cursor: pointer;
        padding: 5px 9px;
        border-radius: 6px;
    }
    .tool-icon:hover {
        background: #F1F5F9;
        color: #1E293B;
    }
    .tool-icon.active {
        background: #EFF6FF;
        color: #3B82F6;
    }
    .tool-divider {
        width: 1px;
        height: 20px;
        background: #E2E8F0;
        margin: 0 6px;
    }
    .zoom-label {
        font-size: 13px;
        font-weight: 500;
        color: #334155;
        padding: 5px 6px;
        cursor: pointer;
    }

    /* Canvas Area */
    .canvas-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        height: 460px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .canvas-image {
        width: 100%;
        height: 100%;
        background: url('MOUNTAIN_IMG_URL') center/cover;
        position: relative;
    }
    .time-chip {
        position: absolute;
        bottom: 10px;
        right: 12px;
        background: rgba(0,0,0,0.6);
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 500;
    }

    /* Drag handle above timeline */
    .drag-handle-row {
        display: flex;
        justify-content: center;
        padding: 4px 0;
    }
    .drag-handle {
        width: 40px;
        height: 4px;
        border-radius: 2px;
        background: #CBD5E1;
    }

    /* Timeline Section */
    .timeline-box {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 12px 20px 18px 20px;
        display: flex;
        flex-direction: column;
        gap: 14px;
    }
    .timeline-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        color: #475569;
    }
    .show-timing {
        background: white;
        border: 1px solid #E2E8F0;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 500;
        cursor: pointer;
    }
    .play-time-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .play-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #3B82F6;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        cursor: pointer;
    }
    .time-badge {
        font-family: monospace;
        font-weight: 600;
        color: #1E293B;
        font-size: 13px;
    }
    .time-badge span {
        color: #3B82F6;
    }
    .zoom-slider-group {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        color: #334155;
    }
    .timeline-track {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .clip-thumbnail {
        width: 320px;
        height: 78px;
        border: 2px solid #3B82F6;
        border-radius: 8px;
        background: linear-gradient(90deg, rgba(59,130,246,0.85), rgba(29,78,216,0.85)), url('MOUNTAIN_IMG_URL') center/cover;
        position: relative;
    }
    .clip-marker {
        position: absolute;
        top: -14px;
        left: 6px;
        width: 0;
        height: 0;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 8px solid #3B82F6;
    }
    .add-clip-btn {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #EFF6FF;
        color: #3B82F6;
        border: none;
        font-size: 18px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }

    /* Right AI Panel */
    .ai-panel {
        background: white;
        border-left: 1px solid #E2E8F0;
        height: calc(100vh - 104px);
        padding: 18px;
        display: flex;
        flex-direction: column;
        gap: 14px;
        overflow-y: auto;
    }
    .ai-panel-header {
        display: flex;
        align-items: center;
        gap: 8px;
        justify-content: space-between;
        font-weight: 600;
        font-size: 15px;
        color: #1E293B;
    }
    .ai-panel-header .left {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .close-x {
        color: #94A3B8;
        cursor: pointer;
        font-size: 15px;
    }
    .preview-card {
        border-radius: 12px;
        overflow: hidden;
    }
    .preview-image {
        height: 180px;
        background: url('MOUNTAIN_IMG_URL') center/cover;
        border-radius: 10px;
        position: relative;
    }
    .action-row {
        display: flex;
        justify-content: space-between;
        margin-top: 12px;
        font-size: 13px;
        font-weight: 500;
        color: #334155;
    }
    .action-row span {
        display: flex;
        align-items: center;
        gap: 5px;
        cursor: pointer;
        padding: 4px 6px;
        border-radius: 6px;
    }
    .action-row span:hover {
        background: #F1F5F9;
    }
    .tabs-row {
        display: flex;
        align-items: center;
        gap: 20px;
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 10px;
        margin-top: 6px;
    }
    .tab-pill {
        display: flex;
        align-items: center;
        gap: 5px;
        cursor: pointer;
    }
    .tab-pill.active {
        background: #EFF6FF;
        color: #3B82F6;
        padding: 6px 12px;
        border-radius: 20px;
    }
    .prompt-text {
        font-size: 14px;
        color: #1E293B;
        padding: 10px 2px;
        min-height: 40px;
    }
    .prompt-thumb {
        width: 70px;
        height: 70px;
        border-radius: 8px;
        background: url('MOUNTAIN_IMG_URL') center/cover;
        border: 1px solid #E2E8F0;
    }
    .prompt-bottom-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
    }
    .model-pill {
        font-size: 12px;
        color: #475569;
        background: #F1F5F9;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 500;
        cursor: pointer;
    }
    .prompt-actions {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .clear-link {
        font-size: 13px;
        color: #3B82F6;
        font-weight: 600;
        cursor: pointer;
    }
    .submit-circle {
        background: #3B82F6;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        cursor: pointer;
    }

    /* Far Right Icon Bar */
    .icon-sidebar {
        background: white;
        border-left: 1px solid #E2E8F0;
        height: calc(100vh - 104px);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 18px;
        gap: 20px;
    }
    .icon-nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        color: #475569;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none;
    }
    .icon-nav-item:hover { color: #1E293B; }
    .icon-nav-item .glyph {
        font-size: 18px;
    }
    .icon-nav-item.active { color: #3B82F6; }
</style>
""".replace("MOUNTAIN_IMG_URL", MOUNTAIN_IMG),
    unsafe_allow_html=True,
)

# ---------------------------
# Top Header Bar
# ---------------------------
st.markdown(
    """
<div class="topbar">
    <div class="logo-area">
        <div class="logo-badge">▶</div>
        <div class="title-block">
            Untitled video
            <span class="title-icon">☆</span>
            <span class="title-icon">📁</span>
            <span class="title-icon">☁️</span>
        </div>
        <div class="menu">
            <span class="tool-icon">File</span>
            <span class="tool-icon">Edit</span>
            <span class="tool-icon">View</span>
            <span class="tool-icon">Insert</span>
            <span class="tool-icon">Format</span>
            <span class="tool-icon">Scene</span>
            <span class="tool-icon">Arrange</span>
            <span class="tool-icon">Tools</span>
            <span class="tool-icon">Help</span>
        </div>
    </div>
    <div class="top-actions">
        <span class="icon-btn">🕐</span>
        <span class="icon-btn">💬</span>
        <button class="btn-play-outline">▶ Play</button>
        <button class="btn-share-solid">🔒 Share ▾</button>
        <div class="avatar-circle">🦊</div>
    </div>
</div>
<div class="sub-toolbar">
    <span class="tool-icon">🔍</span>
    <span class="tool-icon">➕</span>
    <span class="tool-icon">↩</span>
    <span class="tool-icon">↪</span>
    <span class="zoom-label">Fit ▾</span>
    <span class="tool-icon">⌃</span>
    <div class="tool-divider"></div>
    <span class="tool-icon active">↖</span>
    <span class="tool-icon">⬚</span>
    <span class="tool-icon">🖼️</span>
    <span class="tool-icon">🎨</span>
    <span class="tool-icon">🖌️</span>
    <div class="tool-divider"></div>
    <span class="tool-icon">🔗</span>
    <span class="tool-icon">⛓️</span>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Workspace Grid Columns
# ---------------------------
col_workspace, col_aipanel, col_iconbar = st.columns([6, 3, 1], gap="small")

# Center Canvas and Timeline Workspace
with col_workspace:
    st.markdown(
        """
    <div style="padding: 18px; display: flex; flex-direction: column;">
        <div class="canvas-box">
            <div class="canvas-image">
                <div class="time-chip">0:08</div>
            </div>
        </div>

        <div class="drag-handle-row"><div class="drag-handle"></div></div>

        <div class="timeline-box">
            <div class="timeline-controls">
                <span class="show-timing">☰ Show timing ▾</span>
                <div class="play-time-group">
                    <div class="play-circle">▶</div>
                    <div class="time-badge"><span>00:08.0</span> / 00:08.0</div>
                </div>
                <div class="zoom-slider-group">
                    <span>—</span>
                    <input type="range" min="0" max="100" value="60" style="width: 90px; accent-color: #3B82F6;" />
                    <span>+</span>
                    <strong>100% ▾</strong>
                </div>
            </div>
            <div class="timeline-track">
                <div class="clip-thumbnail">
                    <div class="clip-marker"></div>
                </div>
                <button class="add-clip-btn">+</button>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Right AI Inspector Panel
with col_aipanel:
    st.markdown(
        """
    <div class="ai-panel">
        <div class="ai-panel-header">
            <div class="left">🎬 AI video clip</div>
            <span class="close-x">✕</span>
        </div>

        <div class="preview-card">
            <div class="preview-image">
                <div class="time-chip">0:08</div>
            </div>
            <div class="action-row">
                <span>← Insert</span>
                <span>⤢ Extend</span>
                <span>🔄 Recreate</span>
                <span>🗑 Remove</span>
            </div>
        </div>

        <div>
            <div class="tabs-row">
                <span class="tab-pill">✨ Create</span>
                <span class="tab-pill">✏️ Edit</span>
                <span class="tab-pill">🪄 Animate</span>
                <span class="tab-pill active">⤢ Extend ▾</span>
            </div>
            <div class="prompt-text">attack goat</div>
            <div class="prompt-thumb"></div>
            <div class="prompt-bottom-row">
                <span class="model-pill">Veo 3.1 ▾</span>
                <div class="prompt-actions">
                    <span class="clear-link">Clear</span>
                    <div class="submit-circle">↑</div>
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Far Right Tool Icon Column
with col_iconbar:
    st.markdown(
        """
    <div class="icon-sidebar">
        <div class="icon-nav-item active">
            <span class="glyph">🎬</span>
            <span>AI Video</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">👤</span>
            <span>Avatar</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">🎙️</span>
            <span>Voiceover</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">🖼️</span>
            <span>Image</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">⏺️</span>
            <span>Record</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">📁</span>
            <span>Uploads</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">📈</span>
            <span>Stock</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">💬</span>
            <span>Captions</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">T</span>
            <span>Text</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">🗂️</span>
            <span>Templates</span>
        </div>
        <div class="icon-nav-item">
            <span class="glyph">⭐</span>
            <span>Shapes</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
