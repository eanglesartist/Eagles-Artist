from pydantic import BaseModel

# 1. Define the JSON body structure
class GenerateRequest(BaseModel):
    prompt: str
    user_id: str
    model: str = "veo"

# 2. Use the model in the function (request: GenerateRequest)
@app.post("/ai/generate")
def generate_video(request: GenerateRequest):
    credits = get_user_credits(request.user_id)
    # ... rest of your generation logic
