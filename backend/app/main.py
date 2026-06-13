"""Point d'entrée de l'API RECRUT'IA.

Lancement :  uvicorn app.main:app --reload
Documentation interactive : http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import analyses, auth, offres

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RECRUT'IA",
    description="Assistant de recrutement : analyseur de CV intelligent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://recrutia-eight.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router)
app.include_router(offres.router)
app.include_router(analyses.router)


@app.get("/api/sante", tags=["Supervision"])
def sante():
    return {"etat": "ok"}
