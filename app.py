import streamlit as st

st.set_page_config(page_title="AI Cinematic Studio", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Professional Cinematic CSS
# ---------------------------
st.markdown(
    """
<style>
    /* Global Reset & Dark Theme */
    .main .block-container { padding: 0; max-width: 100%; background: #0B0F19; font-family: 'Inter', sans-serif; }
    header {visibility: hidden;}
    
    /* Top Menu Bar */
    .studio-topbar {
        background: #111827;
        border-bottom: 1px solid #1F2937;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        color: #D1D5DB;
        font-size: 13px;
    }
    
    /* Panels */
    .panel {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 16px;
        color: #F3F4F6;
    }
    .director-panel {
        height: calc(100vh - 80px);
        overflow-y: auto;
        margin: 15px 15px 15px 0;
    }
    .canvas-panel {
        height: 500px;
        margin: 15px 15px 15px 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        background: black;
    }
    .timeline-panel {
        height: 200px;
        margin: 0 15px 15px 15px;
    }

    /* Mode Tabs (MV / Movie / Short) */
    .mode-tabs {
        display: flex;
        background: #1F2937;
        border-radius: 8px;
        padding: 4px;
        margin-bottom: 20px;
    }
    .tab {
        flex: 1;
        text-align: center;
        padding: 8px 0;
        font-size: 12px;
        font-weight: 600;
        border-radius: 6px;
        color: #9CA3AF;
        cursor: pointer;
    }
    .tab.active { background: #3B82F6; color: white; }

    /* Setting Blocks */
    .block-title {
        font-size: 11px;
        text-transform: uppercase;
        color: #9CA3AF;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    .input-box {
        width: 100%;
        background: #0B0F19;
        border: 1px solid #374151;
        border-radius: 8px;
        color: white;
        padding: 10px;
        font-size: 13px;
        margin-bottom: 15px;
    }

    /* Grid for Camera Controls */
    .ctrl-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 15px;
    }
    .ctrl-select {
        background: #0B0F19;
        border: 1px solid #374151;
        color: #D1D5DB;
        padding: 8px;
        border-radius: 6px;
        font-size: 11px;
        display: flex;
        justify-content: space-between;
        cursor: pointer;
    }

    /* Extend Feature UI */
    .extend-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid #3B82F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 15px;
    }
    .extend-options {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
    }
    .ext-pill {
        background: #1E3A8A;
        color: #93C5FD;
        font-size: 10px;
        padding: 4px 8px;
        border-radius: 12px;
    }

    /* Buttons */
    .btn-gen {
        background: #3B82F6;
        color: white;
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        margin-bottom: 8px;
    }
    .btn-gen:hover { background: #2563EB; }
    
    .btn-secondary {
        background: #1F2937;
        color: white;
        width: 100%;
        padding: 12px;
        border: 1px solid #374151;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
    }

    /* Timeline Styling */
    .track-container {
        display: flex;
        align-items: center;
        gap: 2px;
        margin-top: 15px;
        background: #0B0F19;
        padding: 10px;
        border-radius: 8px;
        overflow-x: auto;
    }
    .clip {
        height: 60px;
        background: #374151;
        border-radius: 4px;
        min-width: 120px;
        display: flex;
        align-items: flex-end;
        padding: 6px;
        font-size: 10px;
        color: #9CA3AF;
        border-left: 2px solid transparent;
    }
    .clip.active { border-color: #3B82F6; background: #1F2937; color: white; }
    .clip.extend { border-color: #10B981; background: rgba(16, 185, 129, 0.1); }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Top Bar
# ---------------------------
st.markdown(
    """
<div class="studio-topbar">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 16px;">🎬</span>
        <strong style="color: white;">Cinematic Studio</strong>
        <span style="color: #6B7280;">|</span>
        <span>File</span>
        <span>Edit</span>
        <span>View</span>
        <span>Export</span>
    </div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span style="background: #374151; padding: 4px 10px; border-radius: 12px; font-size: 11px;">1080p • 24fps • 2.35:1</span>
        <span>Account ▼</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Layout Grid
# ---------------------------
col_main, col_sidebar = st.columns([7, 3], gap="small")

# Main Area: Canvas + Timeline
with col_main:
    st.markdown(
        """
<div class="panel canvas-panel">
    <div style="position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 4px; font-size: 12px; color: white;">00:00:12:00</div>
    <div style="color: #4B5563; font-size: 14px;">[ Video Preview Canvas - Scene 3 ]</div>
</div>

<div class="panel timeline-panel">
    <div style="display: flex; justify-content: space-between;">
        <div class="block-title">Master Timeline</div>
        <div style="font-size: 12px; color: #9CA3AF;">🔍 Zoom</div>
    </div>
    
    <div class="track-container">
        <div class="clip">Scene 1 (4s)</div>
        <div class="clip extend">↳ Extend (+4s)</div>
        <div class="clip extend">↳ Extend (+4s)</div>
        <div class="clip active" style="min-width: 180px;">Scene 2 - Current</div>
        <div class="clip" style="display: flex; justify-content: center; align-items: center; background: transparent; border: 1px dashed #374151; cursor: pointer;">+ Add Scene</div>
    </div>
    <div style="margin-top: 15px; font-size: 11px; color: #6B7280; display: flex; gap: 15px;">
        <span>🎵 Audio: Auto-Beat Sync Active</span>
        <span>🎨 LUT: Cinematic Teal & Orange</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

# Right Area: AI Director Panel
with col_sidebar:
    st.markdown(
        """
<div class="panel director-panel">
    <div class="mode-tabs">
        <div class="tab">MV Mode</div>
        <div class="tab active">Movie Mode</div>
        <div class="tab">Shorts</div>
    </div>

    <!-- AI Story / Prompt -->
    <div class="block-title">AI Director Prompt</div>
    <textarea class="input-box" style="height: 100px; resize: none;" placeholder="A detective enters an abandoned subway station. Neon lights flicker in the puddles..."></textarea>
    
    <!-- References -->
    <div class="block-title">Reference Memory</div>
    <div class="ctrl-grid">
        <div class="ctrl-select"><span>Character</span><span>🔒 Lock</span></div>
        <div class="ctrl-select"><span>Location</span><span>📍 Set</span></div>
    </div>

    <!-- Camera Controls -->
    <div class="block-title">Cinematography</div>
    <div class="ctrl-grid">
        <div class="ctrl-select"><span>Camera</span><span>ARRI Alexa ▼</span></div>
        <div class="ctrl-select"><span>Lens</span><span>35mm ▼</span></div>
        <div class="ctrl-select"><span>Movement</span><span>Dolly In ▼</span></div>
        <div class="ctrl-select"><span>Style</span><span>Noir ▼</span></div>
    </div>
    <div class="ctrl-grid">
        <div class="ctrl-select"><span>FPS</span><span>24 ▼</span></div>
        <div class="ctrl-select"><span>Shutter</span><span>180° ▼</span></div>
    </div>

    <!-- Video Extend Core Feature -->
    <div class="extend-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div class="block-title" style="color: #60A5FA; margin: 0;">🚀 Video Extend (+4s)</div>
            <input type="checkbox" checked style="accent-color: #3B82F6;">
        </div>
        <div style="font-size: 11px; color: #93C5FD; margin-bottom: 8px;">Preserve continuity from the last frame.</div>
        <div class="extend-options">
            <span class="ext-pill">✓ Motion</span>
            <span class="ext-pill">✓ Camera Pan</span>
            <span class="ext-pill">✓ Identity</span>
            <span class="ext-pill">✓ Lighting</span>
        </div>
        <input type="text" class="input-box" style="margin-top: 10px; margin-bottom: 0; padding: 6px; font-size: 11px;" placeholder="Optional: Alter prompt (e.g., 'He looks behind him')">
    </div>

    <!-- Actions -->
    <button class="btn-gen">✨ Generate Scene</button>
    <div style="display: flex; gap: 8px;">
        <button class="btn-secondary" style="flex: 1;">⤢ Extend</button>
        <button class="btn-secondary" style="flex: 1;">⬆ Upscale</button>
    </div>
    <button class="btn-secondary" style="margin-top: 8px;">📤 Export to MP4 (H.265)</button>

</div>
""",
        unsafe_allow_html=True,
    )
