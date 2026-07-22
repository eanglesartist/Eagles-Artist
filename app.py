import streamlit as st

st.set_page_config(page_title="Cinematic Studio", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Advanced Cinematic CSS
# ---------------------------
st.markdown(
    """
    <style>
        .main .block-container { padding: 0; max-width: 100%; background: #0F172A; } /* Dark mode for video editing */
        header {visibility: hidden;}
        
        .panel-dark {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 16px;
            height: calc(100vh - 40px);
            padding: 20px;
            color: #F8FAFC;
            overflow-y: auto;
            margin: 20px 20px 20px 0;
        }
        
        /* Segmented Control for Project Type */
        .project-type-container {
            display: flex;
            background: #0F172A;
            border-radius: 10px;
            padding: 4px;
            margin-bottom: 20px;
        }
        .pt-btn {
            flex: 1;
            text-align: center;
            padding: 8px 0;
            font-size: 12px;
            font-weight: 600;
            border-radius: 6px;
            color: #94A3B8;
            cursor: pointer;
        }
        .pt-btn.active {
            background: #3B82F6;
            color: white;
        }

        /* Settings Blocks */
        .setting-block {
            background: #0F172A;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 16px;
        }
        .setting-title {
            font-size: 11px;
            text-transform: uppercase;
            color: #94A3B8;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }
        
        /* Grid for Camera/Format */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        .grid-item {
            background: #1E293B;
            border: 1px solid #334155;
            padding: 8px;
            border-radius: 6px;
            font-size: 12px;
            text-align: center;
            color: #CBD5E1;
            cursor: pointer;
        }
        .grid-item:hover { border-color: #3B82F6; }
        .grid-item.active { border-color: #3B82F6; background: rgba(59,130,246,0.1); color: #60A5FA;}

        /* Extend Timeline UI */
        .extend-viz {
            display: flex;
            align-items: center;
            gap: 4px;
            margin-top: 10px;
        }
        .frame-box {
            height: 40px;
            flex: 1;
            background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=100&q=80') center/cover;
            border-radius: 4px;
            opacity: 0.5;
        }
        .frame-box.new {
            background: #3B82F6;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: white;
            opacity: 1;
            border: 2px dashed #93C5FD;
        }

        /* Big Generate Button */
        .btn-generate {
            width: 100%;
            background: linear-gradient(135deg, #3B82F6, #2563EB);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(37,99,235,0.3);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Layout
# ---------------------------
col_workspace, col_aipanel = st.columns([7, 3], gap="small")

with col_workspace:
    st.markdown("<div style='height: 100vh; display:flex; align-items:center; justify-content:center; color:#64748B;'>[ Timeline and Canvas Area - Dark Mode ]</div>", unsafe_allow_html=True)

with col_aipanel:
    # Notice how the HTML tags below are pushed all the way to the left side of the screen
    # This prevents Streamlit from interpreting them as a "code block"
    st.markdown(
        """
<div class="panel-dark">
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="font-weight: 600; font-size: 16px;">🎬 Cinematic Studio</div>
        <span style="font-size: 12px; background: #334155; padding: 4px 10px; border-radius: 20px; color:#93C5FD;">Veo 3.1 Pro</span>
    </div>

    <!-- Project Type -->
    <div class="project-type-container">
        <div class="pt-btn active">Movie</div>
        <div class="pt-btn">Music Video</div>
        <div class="pt-btn">Short Film</div>
    </div>

    <!-- Prompt Engine -->
    <div class="setting-block">
        <div class="setting-title">Scene Description</div>
        <textarea style="width: 100%; height: 80px; background: #1E293B; border: 1px solid #334155; border-radius: 8px; color: white; padding: 10px; font-family: inherit; resize: none;" placeholder="Describe the shot, lighting, and subject..."></textarea>
        <div style="display: flex; gap: 8px; margin-top: 10px;">
            <span style="font-size: 10px; background: #334155; padding: 4px 8px; border-radius: 4px; color: #CBD5E1;">+ Add Style</span>
            <span style="font-size: 10px; background: #334155; padding: 4px 8px; border-radius: 4px; color: #CBD5E1;">+ Negative Prompt</span>
        </div>
    </div>

    <!-- Camera & Format Controls -->
    <div class="setting-block">
        <div class="setting-title">Cinematography</div>
        <div class="grid-2" style="margin-bottom: 12px;">
            <div class="grid-item active">🎥 Pan Right</div>
            <div class="grid-item">🎥 Zoom In</div>
            <div class="grid-item">🚁 Drone/FPV</div>
            <div class="grid-item">✋ Handheld</div>
        </div>
        
        <div class="setting-title" style="margin-top: 16px;">Aspect Ratio</div>
        <div class="grid-2">
            <div class="grid-item">16:9 (Standard)</div>
            <div class="grid-item active">2.35:1 (Cinema)</div>
        </div>
    </div>

    <!-- Extend / Outpaint Logic -->
    <div class="setting-block" style="border-color: #3B82F6;">
        <div style="display:flex; justify-content:space-between;">
            <div class="setting-title" style="color: #60A5FA;">⤢ Video Extension</div>
            <input type="checkbox" checked style="accent-color: #3B82F6;">
        </div>
        <p style="font-size: 11px; color: #94A3B8; margin-top: 4px; line-height: 1.4;">
            Generate the next 4 seconds using the last frame of the selected clip to maintain character and environment consistency.
        </p>
        <div class="extend-viz">
            <div class="frame-box"></div>
            <div class="frame-box"></div>
            <div class="frame-box"></div>
            <div class="frame-box new">✨</div>
        </div>
    </div>

    <button class="btn-generate">Generate Next Scene (4s)</button>
</div>
""",
        unsafe_allow_html=True,
    )
