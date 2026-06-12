"""Consultation du détail d'une analyse."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import utilisateur_courant
from ..models import Analyse, Utilisateur

router = APIRouter(prefix="/api/analyses", tags=["Analyses"])


@router.get("/{analyse_id}")
def detail_analyse(analyse_id: int, db: Session = Depends(get_db),
                   user: Utilisateur = Depends(utilisateur_courant)):
    analyse = db.get(Analyse, analyse_id)
    if analyse is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Analyse inconnue")
    return analyse.to_dict() | {"entites": analyse.entites}
