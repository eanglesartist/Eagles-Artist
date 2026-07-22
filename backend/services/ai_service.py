import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def enhance_prompt(raw_prompt: str) -> str:
    if not openai.api_key:
        return raw_prompt
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a film director. Expand the prompt into a vivid cinematic description with camera angles, lighting, mood, and movement."},
                {"role": "user", "content": raw_prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI enhancement failed: {e}")
        return raw_prompt
