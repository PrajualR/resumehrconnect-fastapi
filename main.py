from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router as resume_router

app = FastAPI(title="Resume Matcher API")

# Allow CORS for PowerApps or other frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/api")
