import streamlit as st

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="AI Video Editor Workspace",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------
# Custom CSS for Canva/Grok Hybrid Layout
# ---------------------------
st.markdown(
    """
<style>
    /* Reset & layout */
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
        height: 56px;
        padding: 0 16px;
        border-bottom: 1px solid #E2E8F0;
        background: white;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .logo-area {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 600;
        font-size: 15px;
        color: #1E293B;
    }
    .menu {
        display: flex;
        gap: 16px;
        font-size: 13px;
        color: #64748B;
        font-weight: 500;
    }
    .top-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .btn-play {
        background: #0F172A;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 6px 16px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
    }
    .btn-share {
        background: #EFF6FF;
        color: #3B82F6;
        border: 1px solid #BFDBFE;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
    }

    /* Secondary Toolbar */
    .sub-toolbar {
        background: white;
        border-bottom: 1px solid #E2E8F0;
        padding: 6px 16px;
        display: flex;
        gap: 16px;
        font-size: 13px;
        color: #64748B;
        align-items: center;
        height: 40px;
    }
    .tool-icon {
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 4px;
    }
    .tool-icon:hover {
        background: #F1F5F9;
        color: #1E293B;
    }

    /* Canvas Area */
    .canvas-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        height: 440px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        margin-bottom: 12px;
    }

    /* Timeline Section */
    .timeline-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        height: 140px;
        padding: 14px 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .timeline-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        color: #64748B;
    }
    .time-badge {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: monospace;
        font-weight: 600;
        color: #3B82F6;
    }
    .timeline-track {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .clip-thumbnail {
        width: 220px;
        height: 60px;
        border: 2px solid #3B82F6;
        border-radius: 8px;
        background: linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: 600;
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
        height: calc(100vh - 96px);
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 14px;
        overflow-y: auto;
    }
    .ai-panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        font-size: 14px;
        color: #1E293B;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 10px;
    }
    .preview-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 10px;
    }
    .action-chips {
        display: flex;
        gap: 6px;
        margin-top: 8px;
    }
    .chip {
        background: white;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 500;
        color: #64748B;
        cursor: pointer;
    }
    .chip:hover {
        border-color: #3B82F6;
        color: #3B82F6;
    }
    .prompt-input-area {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px;
    }

    /* Far Right Icon Bar */
    .icon-sidebar {
        background: white;
        border-left: 1px solid #E2E8F0;
        height: calc(100vh - 96px);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 10px;
        gap: 16px;
    }
    .icon-nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        font-size: 9px;
        color: #64748B;
        cursor: pointer;
        text-decoration: none;
    }
    .icon-nav-item:hover { color: #1E293B; }
    .icon-box {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        font-size: 14px;
    }
    .icon-nav-item.active .icon-box {
        background: #EFF6FF;
        border-color: #BFDBFE;
        color: #3B82F6;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Top Header Bar
# ---------------------------
st.markdown(
    """
<div class="topbar">
    <div class="logo-area">
        <span>🎬</span> Untitled video <span style="font-size: 12px; color: #94A3B8; cursor: pointer;">☆</span>
        <div class="menu" style="margin-left: 20px;">
            <span class="tool-icon">File</span>
            <span class="tool-icon">Edit</span>
            <span class="tool-icon">View</span>
            <span class="tool-icon">Insert</span>
            <span class="tool-icon">Format</span>
            <span class="tool-icon">Scene</span>
            <span class="tool-icon">Tools</span>
        </div>
    </div>
    <div class="top-actions">
        <span style="font-size: 16px; cursor: pointer;">💬</span>
        <button class="btn-play">▶ Play</button>
        <button class="btn-share">🔒 Share ▾</button>
        <div style="width: 30px; height: 30px; background: #EC4899; border-radius: 50%;"></div>
    </div>
</div>
<div class="sub-toolbar">
    <span>🔍 ➕ ↩ ↪ ✨ Fit</span>
    <span>|</span>
    <span>↖ ➕ 🖼️ 🎨 🖌️</span>
    <span>|</span>
    <span>💧 🔗</span>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Workspace Grid Columns (Canvas/Timeline | AI Panel | Icon Bar)
# ---------------------------
col_workspace, col_aipanel, col_iconbar = st.columns([6, 3, 1], gap="small")

# Center Canvas and Timeline Workspace
with col_workspace:
    st.markdown(
        """
    <div style="padding: 16px; display: flex; flex-direction: column; gap: 12px;">
        <div class="canvas-box">
            <div style="width: 75%; height: 80%; background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80') center/cover; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative;">
                <div style="position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.6); color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px;">00:08</div>
            </div>
        </div>
        
        <div class="timeline-box">
            <div class="timeline-controls">
                <span style="background: #F1F5F9; padding: 4px 10px; border-radius: 6px; cursor: pointer;">⏱ Show timing ▾</span>
                <div class="time-badge">▶ 00:08.0 / 00:08.0</div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                    <span>—</span>
                    <input type="range" min="0" max="100" value="60" style="width: 80px; accent-color: #3B82F6;" />
                    <span>+</span>
                    <strong>100% ▾</strong>
                </div>
            </div>
            <div class="timeline-track">
                <div class="clip-thumbnail">
                    <span>🎬 Mountain Flight (Clip 1)</span>
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
            <span>✨ AI video clip</span>
            <span style="cursor: pointer; color: #94A3B8;">✕</span>
        </div>
        
        <div class="preview-card">
            <div style="height: 130px; background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=400&q=80') center/cover; border-radius: 8px; position: relative;">
                <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(0,0,0,0.7); color: white; font-size: 10px; padding: 2px 4px; border-radius: 3px;">0:08</span>
            </div>
            <div class="action-chips">
                <span class="chip">← Insert</span>
                <span class="chip">⤢ Extend</span>
                <span class="chip">🔄 Recreate</span>
                <span class="chip">🗑 Remove</span>
            </div>
        </div>

        <div class="prompt-input-area">
            <div style="display: flex; gap: 8px; font-size: 12px; font-weight: 600; margin-bottom: 8px;">
                <span style="color: #3B82F6; border-bottom: 2px solid #3B82F6; padding-bottom: 2px;">🟦 Create</span>
                <span style="color: #64748B;">✏️ Edit</span>
                <span style="color: #64748B;">✨ Animate</span>
            </div>
            <div style="font-size: 13px; color: #1E293B; background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px; min-height: 50px;">
                attack goat
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <span style="font-size: 11px; color: #64748B; background: #F1F5F9; padding: 4px 8px; border-radius: 4px;">Veo 3.1 ▾</span>
                <div style="display: flex; gap: 6px;">
                    <span style="font-size: 11px; padding: 6px 10px; border: 1px solid #E2E8F0; border-radius: 20px; cursor: pointer;">Clear</span>
                    <span style="background: #3B82F6; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; cursor: pointer;">↑</span>
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
            <div class="icon-box">🎬</div>
            <span>AI Video</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">👤</div>
            <span>Avatar</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">🎙️</div>
            <span>Voice</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">🎵</div>
            <span>Music</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">🖼️</div>
            <span>Image</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">⏺️</div>
            <span>Record</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">📁</div>
            <span>Uploads</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">📈</div>
            <span>Stock</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">💬</div>
            <span>Captions</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">T</div>
            <span>Text</span>
        </div>
        <div class="icon-nav-item">
            <div class="icon-box">⭐</div>
            <span>Shapes</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
