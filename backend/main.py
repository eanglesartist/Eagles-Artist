from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import credits, projects, assets, ai, webhooks
from .database import engine, Base

# Create tables (if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Cinematic Studio API", version="2.0")

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(credits.router)
app.include_router(projects.router)
app.include_router(assets.router)
app.include_router(ai.router)
app.include_router(webhooks.router)

@app.get("/")
def root():
    return {"message": "AI Cinematic Studio API is running"}
