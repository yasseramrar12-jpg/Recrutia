"""Authentification : POST /api/auth/login."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Utilisateur
from ..schemas import ConnexionReponse, ConnexionRequete
from ..securite import creer_jeton, verifier_mot_de_passe

router = APIRouter(prefix="/api/auth", tags=["Authentification"])


@router.post("/login", response_model=ConnexionReponse)
def connexion(requete: ConnexionRequete, db: Session = Depends(get_db)):
    utilisateur = db.scalar(select(Utilisateur).where(Utilisateur.email == requete.email))
    if utilisateur is None or not verifier_mot_de_passe(requete.mot_de_passe, utilisateur.mot_de_passe_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Identifiants invalides")
    return ConnexionReponse(
        jeton=creer_jeton(utilisateur.id, utilisateur.role),
        nom=utilisateur.nom,
        role=utilisateur.role,
    )
