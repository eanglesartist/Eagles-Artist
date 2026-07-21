"""
scene_generator.py
-------------------
Splits a longer story prompt into an ordered list of scenes, each of
which becomes one Timeline scene (see database/timeline_model.py).
"""
import re
from ai_engine.prompt_builder import expand_prompt


def split_into_scenes(story_prompt: str, max_scenes: int = 6) -> list[str]:
    """Naive sentence-based split; replace with an LLM scene planner later."""
    sentences = re.split(r"(?<=[.!?])\s+", (story_prompt or "").strip())
    return [s for s in sentences if s][:max_scenes]


def build_scene_plan(story_prompt: str, max_scenes: int = 6) -> list[dict]:
    """Returns a list of scene dicts ready to drop into the timeline."""
    scenes = split_into_scenes(story_prompt, max_scenes)
    plan = []
    for i, raw in enumerate(scenes, start=1):
        plan.append(
            {
                "id": f"scene-{i}",
                "raw_prompt": raw,
                "expanded_prompt": expand_prompt(raw),
                "duration": 8,
            }
        )
    return plan
