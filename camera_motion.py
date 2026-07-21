"""
camera_motion.py
------------------
Suggests a camera motion plan for a scene based on its content and
the chosen editing sub-action (Change Camera, etc).
"""
import random

MOTION_LIBRARY = {
    "static": "Locked-off static shot",
    "pan_left": "Slow pan left",
    "pan_right": "Slow pan right",
    "dolly_in": "Dolly in toward subject",
    "dolly_out": "Dolly out revealing environment",
    "orbit": "Orbit around subject",
    "crane_up": "Crane up and away",
    "handheld": "Handheld tracking shot",
}


def suggest_motion(scene_prompt: str) -> dict:
    """Very light heuristic: action words -> more dynamic camera motion."""
    prompt_lower = (scene_prompt or "").lower()
    dynamic_keywords = ["run", "attack", "fight", "chase", "fly", "race"]

    if any(k in prompt_lower for k in dynamic_keywords):
        choice = random.choice(["dolly_in", "orbit", "handheld", "crane_up"])
    else:
        choice = random.choice(["static", "pan_left", "pan_right", "dolly_out"])

    return {"motion_id": choice, "label": MOTION_LIBRARY[choice]}


def change_camera(scene_prompt: str, motion_id: str) -> dict:
    """Used by the 'Edit Video -> Change Camera' action."""
    label = MOTION_LIBRARY.get(motion_id, MOTION_LIBRARY["static"])
    return {"motion_id": motion_id, "label": label, "scene_prompt": scene_prompt}
