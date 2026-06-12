"""Hachage des mots de passe et jetons JWT."""
import hashlib
import os
from datetime import datetime, timedelta, timezone

import jwt

from .config import DUREE_JETON_MINUTES, SECRET_JWT

_ITERATIONS = 200_000


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    sel = os.urandom(16)
    empreinte = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode(), sel, _ITERATIONS)
    return f"pbkdf2${_ITERATIONS}${sel.hex()}${empreinte.hex()}"


def verifier_mot_de_passe(mot_de_passe: str, stocke: str) -> bool:
    try:
        _, iterations, sel_hex, empreinte_hex = stocke.split("$")
        empreinte = hashlib.pbkdf2_hmac(
            "sha256", mot_de_passe.encode(), bytes.fromhex(sel_hex), int(iterations)
        )
        return empreinte.hex() == empreinte_hex
    except ValueError:
        return False


def creer_jeton(utilisateur_id: int, role: str) -> str:
    charge = {
        "sub": str(utilisateur_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=DUREE_JETON_MINUTES),
    }
    return jwt.encode(charge, SECRET_JWT, algorithm="HS256")


def decoder_jeton(jeton: str) -> dict:
    return jwt.decode(jeton, SECRET_JWT, algorithms=["HS256"])
