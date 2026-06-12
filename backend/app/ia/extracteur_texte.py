"""Extraction et nettoyage du texte des CV PDF (cf. pipeline du dossier technique)."""
import re
import unicodedata

import pdfplumber


class ErreurExtractionPDF(Exception):
    """Levée quand le PDF ne contient pas de texte exploitable (scan, image...)."""


def extraire_pdf(chemin: str) -> str:
    """Extrait le texte brut d'un PDF natif. Lève ErreurExtractionPDF sinon."""
    try:
        with pdfplumber.open(chemin) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
    except Exception as exc:  # PDF corrompu, chiffré...
        raise ErreurExtractionPDF(f"PDF illisible : {exc}") from exc

    texte = "\n".join(pages).strip()
    if len(texte) < 50:
        raise ErreurExtractionPDF(
            "Le PDF ne contient pas de texte exploitable (document scanné ?)."
        )
    return texte


def normaliser(texte: str) -> str:
    """Minuscules, accents supprimés, espaces compactés.

    Utilisé pour la recherche de compétences et la vectorisation TF-IDF.
    """
    texte = texte.lower()
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    texte = re.sub(r"[ \t]+", " ", texte)
    return texte.strip()
