import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from database import db, create_document, get_documents
from schemas import Story, Program, Volunteer, Donation, NewsletterSubscriber

app = FastAPI(title="Favor International API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Favor International Backend Running"}


@app.get("/schema")
def get_schema_info():
    """Return names of available collections (for admin tooling)."""
    return {
        "collections": [
            "story",
            "program",
            "volunteer",
            "donation",
            "newslettersubscriber",
        ]
    }


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = (
                os.getenv("DATABASE_NAME") or (db.name if hasattr(db, "name") else None)
            )
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# -------------------- API Endpoints --------------------
# Stories
@app.get("/api/stories")
async def get_stories(limit: int = 20):
    try:
        docs = get_documents("story", {}, limit)
        # Convert ObjectId to str for JSON
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Programs
@app.get("/api/programs")
async def get_programs(limit: int = 50):
    try:
        docs = get_documents("program", {}, limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Volunteer sign-up
@app.post("/api/volunteer")
async def signup_volunteer(payload: Volunteer):
    try:
        doc_id = create_document("volunteer", payload)
        return {"success": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Newsletter signup (stub for Mailchimp integration)
class NewsletterPayload(BaseModel):
    email: EmailStr


@app.post("/api/newsletter")
async def signup_newsletter(payload: NewsletterPayload):
    try:
        # Save to DB for record-keeping
        sub = NewsletterSubscriber(email=payload.email, subscribed_date=datetime.utcnow())
        create_document("newslettersubscriber", sub)
        # In a real integration, you would also call Mailchimp/Sendgrid API here
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Donation (placeholder, no real payment processing here)
class DonationPayload(BaseModel):
    full_name: str
    email: EmailStr
    amount: float


@app.post("/api/donate")
async def post_donation(payload: DonationPayload):
    try:
        # Here you'd integrate with Stripe/PayPal. We'll just record the intent.
        donation = Donation(
            full_name=payload.full_name,
            email=payload.email,
            amount=payload.amount,
            donation_date=datetime.utcnow(),
        )
        doc_id = create_document("donation", donation)
        return {"success": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
