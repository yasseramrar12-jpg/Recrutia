"""Schémas Pydantic (validation des entrées / sorties de l'API)."""
from pydantic import BaseModel, EmailStr, Field


class ConnexionRequete(BaseModel):
    email: EmailStr
    mot_de_passe: str


class ConnexionReponse(BaseModel):
    jeton: str
    nom: str
    role: str


class OffreCreation(BaseModel):
    titre: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    competences_requises: list[str] = Field(default_factory=list)
    experience_min: int = Field(default=0, ge=0, le=40)


class OffreReponse(BaseModel):
    id: int
    titre: str
    description: str
    competences_requises: list[str]
    experience_min: int
    nb_cvs: int = 0
    nb_analyses: int = 0
