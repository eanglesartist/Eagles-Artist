"""
video_extend.py
------------------
Builds requests for the three "Extend" sub-actions:
Continue Scene, Add Action, Add Ending.
"""

EXTEND_TEMPLATES = {
    "continue_scene": "Continue the current scene naturally for {seconds} more seconds, matching lighting, camera, and motion.",
    "add_action": "Introduce a new action into the scene: {detail}. Keep visual continuity with the last frame.",
    "add_ending": "Bring the scene to a satisfying conclusion in {seconds} seconds, slowing the motion toward the final frame.",
}


def build_extend_request(clip_id: str, mode: str, seconds: int = 4, detail: str = "") -> dict:
    """
    mode: one of "continue_scene", "add_action", "add_ending"
    """
    template = EXTEND_TEMPLATES.get(mode, EXTEND_TEMPLATES["continue_scene"])
    instruction = template.format(seconds=seconds, detail=detail or "a new element entering frame")

    return {
        "clip_id": clip_id,
        "mode": mode,
        "seconds": seconds,
        "instruction": instruction,
    }
