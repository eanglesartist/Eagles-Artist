from fastapi import FastAPI, Request, HTTPException
import stripe
from utils.db import add_credits, transaction_exists

app = FastAPI()

# Load your secret key from environment or a config file
import os
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Or use st.secrets if running inside Streamlit context

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        
        # Idempotency: skip if already processed
        if transaction_exists(session_id):
            return {"status": "already_processed"}

        # Get user_id from metadata you passed when creating the session
        user_id = session.get("metadata", {}).get("user_id", "default_user")
        
        # Map amount to credits (USD cents -> dollars)
        amount_total = session["amount_total"] / 100
        credits_map = {1.0: 50, 5.0: 300, 10.0: 700}
        credits = credits_map.get(amount_total, 0)
        
        if credits > 0:
            add_credits(user_id, credits, session_id)
            print(f"✅ Added {credits} credits to user {user_id} via webhook")

    return {"status": "success"}
