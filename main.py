from fastapi import FastAPI, Request, Header, HTTPException
import stripe
from backend.billing import add_credits_to_database

app = FastAPI()

# Replace with your actual live/test keys or load from environment variables
stripe.api_key = "sk_test_your_stripe_secret_key"
endpoint_secret = "whsec_your_stripe_webhook_signing_secret"

@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the successful checkout session completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Get customer details from Stripe checkout session
        customer_email = session.get("customer_email") or session.get("customer_details", {}).get("email")
        amount_total = session.get("amount_total") # Stored in cents (e.g., 100 = $1.00, 500 = $5.00)
        
        if not customer_email:
            return {"status": "error", "message": "No customer email found"}

        # Map the payment amount to the corresponding credit packages ($1, $5, $10)
        if amount_total == 100:     # $1.00 Pack
            credits_to_add = 50
        elif amount_total == 500:   # $5.00 Pack
            credits_to_add = 300
        elif amount_total == 1000:  # $10.00 Pack
            credits_to_add = 700
        else:
            credits_to_add = 0

        if credits_to_add > 0:
            # Automatically update the database
            add_credits_to_database(customer_email, credits_to_add)

    return {"status": "success"}