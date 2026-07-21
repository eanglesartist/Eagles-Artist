"""
video_api.py
------------------
Dispatches a generation request to the selected AI video provider
(Google Veo, OpenAI Video, Runway, Kling AI, Pika).
"""
from api.providers import AI_VIDEO_PROVIDERS


def generate_video(prompt: str, provider_id: str = "google_veo", **kwargs) -> dict:
    provider = AI_VIDEO_PROVIDERS.get(provider_id, AI_VIDEO_PROVIDERS["google_veo"])

    if not provider["enabled"]:
        # Stub response so the UI has something to render before a real
        # key/provider integration is wired up.
        return {
            "status": "stub",
            "provider": provider["label"],
            "video_url": None,
            "prompt": prompt,
            "duration": kwargs.get("duration", "0:08"),
        }

    # TODO: call the real provider SDK/REST API here.
    raise NotImplementedError(f"{provider['label']} integration not implemented yet")


def extend_video(clip_id: str, instruction: str, provider_id: str = "google_veo") -> dict:
    provider = AI_VIDEO_PROVIDERS.get(provider_id, AI_VIDEO_PROVIDERS["google_veo"])
    return {
        "status": "stub",
        "provider": provider["label"],
        "clip_id": clip_id,
        "instruction": instruction,
        "video_url": None,
    }
