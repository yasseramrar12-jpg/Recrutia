"""Extraction d'entités : compétences, expérience, diplômes, coordonnées.

Deux moteurs sont combinés :
  1. une recherche par référentiel (toujours disponible) ;
  2. le modèle spaCy fr_core_news_md s'il est installé (optionnel),
     utilisé pour repérer le nom du candidat (entités PER).
"""
import re
from datetime import date

from .extracteur_texte import normaliser
from .referentiel import MOTS_DIPLOMES, REFERENTIEL_COMPETENCES

try:  # spaCy est optionnel : le module fonctionne sans.
    import spacy

    try:
        _nlp = spacy.load("fr_core_news_md")
    except OSError:
        _nlp = None
except ImportError:
    _nlp = None

_RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_RE_TELEPHONE = re.compile(r"(?:\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4}")
_RE_ANNEES_EXPLICITES = re.compile(r"(\d{1,2})\s*(?:ans?|années?)\s*d['e ]\s*exp[ée]rience")
_RE_PLAGE_DATES = re.compile(
    r"(?:(?:janv|f[ée]vr|mars|avr|mai|juin|juil|ao[uû]t|sept|oct|nov|d[ée]c)\w*\.?\s+)?"
    r"(\d{4})\s*[-–à>]+\s*"
    r"(?:(?:janv|f[ée]vr|mars|avr|mai|juin|juil|ao[uû]t|sept|oct|nov|d[ée]c)\w*\.?\s+)?"
    r"(\d{4}|aujourd'hui|present|présent|actuel)"
)


def extraire_competences(texte: str) -> list[str]:
    """Retourne les compétences canoniques trouvées dans le texte."""
    texte_norm = " " + normaliser(texte).replace("\n", " ") + " "
    trouvees = []
    for canonique, formes in REFERENTIEL_COMPETENCES.items():
        for forme in formes:
            motif = r"(?<![\w+#])" + re.escape(normaliser(forme)) + r"(?![\w+#])"
            if re.search(motif, texte_norm):
                trouvees.append(canonique)
                break
    return sorted(trouvees)


def extraire_experience(texte: str) -> int:
    """Estime les années d'expérience.

    Priorité à une mention explicite (« 5 ans d'expérience ») ; sinon,
    cumul des plages de dates détectées (bornées à l'année courante).
    """
    texte_norm = normaliser(texte)
    explicites = [int(n) for n in _RE_ANNEES_EXPLICITES.findall(texte_norm)]
    if explicites:
        return min(max(explicites), 45)

    annee_courante = date.today().year
    total = 0
    for debut, fin in _RE_PLAGE_DATES.findall(texte_norm):
        debut = int(debut)
        fin = annee_courante if not fin.isdigit() else int(fin)
        if 1970 <= debut <= fin <= annee_courante:
            total += fin - debut
    return min(total, 45)


def extraire_diplomes(texte: str) -> list[str]:
    texte_norm = normaliser(texte)
    return sorted({mot for mot in MOTS_DIPLOMES if normaliser(mot) in texte_norm})


def extraire_contact(texte: str) -> dict:
    email = _RE_EMAIL.search(texte)
    telephone = _RE_TELEPHONE.search(texte)
    return {
        "email": email.group(0) if email else None,
        "telephone": telephone.group(0).strip() if telephone else None,
    }


def extraire_nom_candidat(texte: str) -> str | None:
    """Nom du candidat : entité PER de spaCy si disponible, sinon 1re ligne plausible."""
    if _nlp is not None:
        doc = _nlp(texte[:1000])
        personnes = [ent.text.strip() for ent in doc.ents if ent.label_ == "PER"]
        if personnes:
            return personnes[0]
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        mots = ligne.split()
        if 1 < len(mots) <= 4 and all(m[:1].isupper() for m in mots if m.isalpha()):
            return ligne
    return None
