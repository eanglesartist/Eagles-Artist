"""
ai_panel.py
------------------
Upgraded AI Video Panel:

Create Video  -> Text→Video / Image→Video / Story→Video / Character Video / Product Video
Edit Video    -> Change Style / Change Camera / Remove Object / Replace Scene
Extend        -> Continue Scene / Add Action / Add Ending

Also renders the Prompt Engine preview (raw prompt -> expanded cinematic prompt)
and the AI video provider picker.
"""
import streamlit as st

from ai_engine.prompt_builder import expand_prompt
from ai_engine.style_engine import list_styles, apply_style
from ai_engine.camera_motion import suggest_motion, change_camera, MOTION_LIBRARY
from ai_engine.video_extend import build_extend_request
from api.providers import AI_VIDEO_PROVIDERS, provider_labels, provider_id_from_label
from api.video_api import generate_video, extend_video

CREATE_SUBACTIONS = ["Text → Video", "Image → Video", "Story → Video", "Character Video", "Product Video"]
EDIT_SUBACTIONS = ["Change Style", "Change Camera", "Remove Object", "Replace Scene"]
EXTEND_SUBACTIONS = ["Continue Scene", "Add Action", "Add Ending"]


def render_ai_panel(active_scene):
    st.markdown('<div class="ai-panel-header">🎬 AI Video Panel</div>', unsafe_allow_html=True)

    top_action = st.radio(
        "Action",
        ["Create Video", "Edit Video", "Extend"],
        horizontal=True,
        label_visibility="collapsed",
        key="ai_panel_top_action",
    )

    provider_label = st.selectbox(
        "AI video provider",
        provider_labels(AI_VIDEO_PROVIDERS),
        key="ai_panel_provider",
    )
    provider_id = provider_id_from_label(AI_VIDEO_PROVIDERS, provider_label)

    if top_action == "Create Video":
        _render_create(active_scene, provider_id)
    elif top_action == "Edit Video":
        _render_edit(active_scene, provider_id)
    else:
        _render_extend(active_scene, provider_id)


def _render_create(active_scene, provider_id):
    sub_action = st.selectbox("Create mode", CREATE_SUBACTIONS, key="create_subaction")

    ref_image = None
    if sub_action == "Image → Video":
        ref_image = st.file_uploader("Reference image", type=["png", "jpg", "jpeg"], key="create_ref_image")
    elif sub_action == "Character Video":
        st.text_input("Character description", placeholder="e.g. a rugged mountain guide, brown jacket", key="character_desc")
    elif sub_action == "Product Video":
        st.text_input("Product name / details", placeholder="e.g. matte black wireless headphones", key="product_desc")

    raw_prompt = st.text_area(
        "Describe the scene",
        placeholder="attack goat",
        key="create_raw_prompt",
        height=80,
    )

    if raw_prompt:
        expanded = expand_prompt(raw_prompt)
        st.markdown(f'<div class="expanded-prompt-box">✨ <b>Expanded prompt</b><br>{expanded}</div>', unsafe_allow_html=True)
    else:
        expanded = ""

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Clear", use_container_width=True, key="create_clear"):
            st.session_state["create_raw_prompt"] = ""
            st.rerun()
    with col2:
        if st.button("↑ Generate", type="primary", use_container_width=True, key="create_generate"):
            if not raw_prompt:
                st.warning("Enter a prompt first.")
            else:
                result = generate_video(expanded, provider_id=provider_id, mode=sub_action)
                active_scene.prompt = raw_prompt
                active_scene.expanded_prompt = expanded
                active_scene.assets.video_url = result.get("video_url")
                st.success(f"Sent to {result['provider']} ({sub_action}). Status: {result['status']}")


def _render_edit(active_scene, provider_id):
    sub_action = st.selectbox("Edit mode", EDIT_SUBACTIONS, key="edit_subaction")

    if sub_action == "Change Style":
        style_id = st.selectbox("Style preset", list_styles(), key="edit_style")
        if st.button("Apply style", key="apply_style_btn"):
            new_prompt = apply_style(active_scene.expanded_prompt or active_scene.prompt, style_id)
            active_scene.expanded_prompt = new_prompt
            active_scene.style = style_id
            st.success(f"Style '{style_id}' applied to scene prompt.")
            st.markdown(f'<div class="expanded-prompt-box">{new_prompt}</div>', unsafe_allow_html=True)

    elif sub_action == "Change Camera":
        motion_id = st.selectbox(
            "Camera motion",
            list(MOTION_LIBRARY.keys()),
            format_func=lambda k: MOTION_LIBRARY[k],
            key="edit_camera_motion",
        )
        if st.button("Apply camera motion", key="apply_camera_btn"):
            result = change_camera(active_scene.expanded_prompt or active_scene.prompt, motion_id)
            active_scene.camera_motion = result["motion_id"]
            st.success(f"Camera motion set to: {result['label']}")

    elif sub_action == "Remove Object":
        obj = st.text_input("Object to remove", placeholder="e.g. the backpack", key="remove_object_input")
        if st.button("Remove object", key="remove_object_btn"):
            if obj:
                active_scene.expanded_prompt = f"{active_scene.expanded_prompt or active_scene.prompt}, remove {obj} from frame"
                st.success(f"Queued object removal: {obj}")
            else:
                st.warning("Describe the object to remove.")

    else:  # Replace Scene
        new_setting = st.text_input("Replace background/setting with", placeholder="e.g. a rainforest at dawn", key="replace_scene_input")
        if st.button("Replace scene", key="replace_scene_btn"):
            if new_setting:
                active_scene.expanded_prompt = f"{active_scene.prompt}, set in {new_setting}"
                st.success("Scene setting replaced.")
            else:
                st.warning("Describe the new setting.")


def _render_extend(active_scene, provider_id):
    sub_action = st.selectbox("Extend mode", EXTEND_SUBACTIONS, key="extend_subaction")
    mode_map = {
        "Continue Scene": "continue_scene",
        "Add Action": "add_action",
        "Add Ending": "add_ending",
    }
    seconds = st.slider("Extra seconds", 2, 10, 4, key="extend_seconds")

    detail = ""
    if sub_action == "Add Action":
        detail = st.text_input("New action to introduce", placeholder="e.g. a second goat joins", key="extend_action_detail")

    if st.button("⤢ Extend clip", type="primary", key="extend_btn"):
        req = build_extend_request(active_scene.id, mode_map[sub_action], seconds, detail)
        result = extend_video(active_scene.id, req["instruction"], provider_id=provider_id)
        active_scene.duration_seconds += seconds
        st.success(f"Extend request sent to {result['provider']}: {req['instruction']}")
