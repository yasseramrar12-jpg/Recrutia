"""Point d'entrée de l'API RECRUT'IA.
Lancement :  uvicorn app.main:app --reload
Documentation interactive : http://localhost:8000/docs
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    "https://recrutia-production-d2db.up.railway.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "https://recrutia-eight.vercel.app",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

app.include_router(auth.router)
app.include_router(offres.router)
app.include_router(analyses.router)

@app.get("/api/sante", tags=["Supervision"])
def sante():
    return {"etat": "ok"}
