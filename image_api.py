"""
image_api.py
------------------
Dispatches to the selected AI image provider (OpenAI Image, Midjourney, Flux).
"""
from api.providers import AI_IMAGE_PROVIDERS


def generate_image(prompt: str, provider_id: str = "openai_image") -> dict:
    provider = AI_IMAGE_PROVIDERS.get(provider_id, AI_IMAGE_PROVIDERS["openai_image"])

    if not provider["enabled"]:
        return {"status": "stub", "provider": provider["label"], "image_url": None, "prompt": prompt}

    # TODO: call the real provider SDK/REST API here.
    raise NotImplementedError(f"{provider['label']} integration not implemented yet")
