"""
main.py
-------
FastAPI backend for the Syntecxhub Data Science Task — Project 2
(Netflix / Media Dataset EDA).

Run with:
    pip install -r requirements.txt
    uvicorn app.main:app --reload
Docs at http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import netflix

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="Syntecxhub Netflix EDA API",
    description="Netflix / media catalog exploratory data analysis backend",
    version="1.0.0",
)

# allow_credentials is False because we use a wildcard origin for easy local
# dev — browsers reject "*" combined with credentialed requests, and this
# API doesn't use cookies/auth, so it isn't needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(netflix.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup_event():
    netflix.ensure_data()
