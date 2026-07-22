from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import add_credits
import stripe
import os

router = APIRouter(prefix="/stripe", tags=["stripe"])

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        user_id = session.get("metadata", {}).get("user_id", "default_user")
        amount_total = session["amount_total"] / 100
        credits_map = {1.0: 50, 5.0: 300, 10.0: 700}
        credits = credits_map.get(amount_total, 0)
        if credits > 0:
            db = next(get_db())
            add_credits(db, user_id, credits, session_id)
            db.close()
    return {"status": "success"}
