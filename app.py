import streamlit as st

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="AI Video Editor",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown(
    """
<style>
    /* Reset some defaults */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
    }

    /* Top bar */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 64px;
        padding: 0 20px;
        border-bottom: 1px solid #ececec;
        background: white;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .logo {
        font-weight: 600;
        font-size: 18px;
        color: #1a1a1a;
    }
    .menu {
        display: flex;
        gap: 18px;
        font-size: 14px;
        color: #333;
        font-weight: 500;
    }
    .actions {
        display: flex;
        gap: 12px;
    }
    .play {
        background: white;
        border: 1px solid #ddd;
        border-radius: 25px;
        padding: 8px 20px;
        font-weight: 600;
        cursor: pointer;
    }
    .share {
        background: #4EA5FF;
        color: white;
        border: none;
        padding: 8px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
    }

    /* Left toolbar */
    .tools {
        display: flex;
        flex-direction: column;
        gap: 22px;
        align-items: center;
        padding-top: 40px;
        font-size: 28px;
        background: white;
        height: 850px;
        border-right: 1px solid #eee;
    }

    /* Center canvas */
    .canvas {
        height: 720px;
        background: #F7F8FA;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 20px;
    }
    .workspace {
        background: white;
        height: 520px;
        border: 1px solid #ddd;
        margin: 0 auto;
        width: 90%;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #aaa;
        font-size: 18px;
    }

    /* Timeline */
    .timeline {
        height: 170px;
        background: #F5F7FA;
        border-radius: 20px;
        padding: 20px;
        display: flex;
        align-items: center;
    }
    .clip {
        width: 300px;
        height: 80px;
        border: 2px solid #4C8DFF;
        border-radius: 15px;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: #4C8DFF;
        font-weight: 500;
    }

    /* Right panel */
    .sidepanel {
        background: white;
        border-left: 1px solid #eee;
        padding: 20px;
        height: 820px;
        overflow-y: auto;
    }
    .sidepanel h2 {
        font-size: 20px;
        margin-top: 0;
        margin-bottom: 20px;
    }
    .thumbgrid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 20px;
    }
    .thumb {
        height: 160px;
        background: #ddd;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #888;
        font-size: 14px;
    }
    .sidepanel textarea {
        width: 100%;
        height: 120px;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #ddd;
        font-family: inherit;
        resize: vertical;
    }
    .sidepanel button {
        width: 100%;
        height: 48px;
        margin-top: 15px;
        background: #4C8DFF;
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: 700;
        cursor: pointer;
    }
    .sidepanel button:hover {
        background: #3a7ae0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Top Navigation
# ---------------------------
st.markdown(
    """
<div class="topbar">
    <div class="logo">▶ Untitled Video</div>
    <div class="menu">
        File Edit View Insert Format Scene Arrange Tools Help
    </div>
    <div class="actions">
        <button class="play">▶ Play</button>
        <button class="share">Share</button>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Three‑column layout
# ---------------------------
left, center, right = st.columns([1, 4, 2], gap="small")

# Left toolbar
with left:
    st.markdown(
        """
<div class="tools">
    🏠
    🎙
    🖼
    🎥
    ⬆
    📁
    ✏
    📄
    🔤
    ⬜
</div>
""",
        unsafe_allow_html=True,
    )

# Center canvas + timeline
with center:
    st.markdown(
        """
<div class="canvas">
    <div class="workspace">
        🎬 Video preview area
    </div>
</div>
<div class="timeline">
    <div class="clip">📹 Clip 1</div>
</div>
""",
        unsafe_allow_html=True,
    )

# Right AI panel
with right:
    st.markdown(
        """
<div class="sidepanel">
    <h2>🎬 AI video clip</h2>
    <div class="thumbgrid">
        <div class="thumb">Thumb 1</div>
        <div class="thumb">Thumb 2</div>
        <div class="thumb">Thumb 3</div>
        <div class="thumb">Thumb 4</div>
    </div>
    <textarea placeholder="Describe your video..."></textarea>
    <button>Create</button>
</div>
""",
        unsafe_allow_html=True,
    )
