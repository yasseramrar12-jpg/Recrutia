"""Dépendances communes : utilisateur courant authentifié."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import Utilisateur
from .securite import decoder_jeton

_schema = HTTPBearer(auto_error=False)


def utilisateur_courant(
    creds: HTTPAuthorizationCredentials = Depends(_schema),
    db: Session = Depends(get_db),
) -> Utilisateur:
    if creds is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Jeton manquant")
    try:
        charge = decoder_jeton(creds.credentials)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Jeton invalide ou expiré")
    utilisateur = db.get(Utilisateur, int(charge["sub"]))
    if utilisateur is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Utilisateur inconnu")
    return utilisateur
