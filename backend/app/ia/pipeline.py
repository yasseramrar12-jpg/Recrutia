"""Pipeline NLP complet : du PDF au score de correspondance.

Implémente le diagramme d'activité du dossier technique :
extraction de texte -> nettoyage -> (entités || similarité) -> score global.
"""
from dataclasses import dataclass, field

from ..config import POIDS_COMPETENCES, POIDS_EXPERIENCE, POIDS_SEMANTIQUE
from . import extracteur_entites as entites
from .extracteur_texte import extraire_pdf
from .similarite import similarite_semantique


@dataclass
class ResultatAnalyse:
    score_global: float = 0.0
    score_competences: float = 0.0
    score_experience: float = 0.0
    score_semantique: float = 0.0
    methode_similarite: str = "tfidf"
    entites: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "score_global": round(self.score_global, 1),
            "score_competences": round(self.score_competences, 3),
            "score_experience": round(self.score_experience, 3),
            "score_semantique": round(self.score_semantique, 3),
            "methode_similarite": self.methode_similarite,
            "entites": self.entites,
        }


def traiter_texte(texte_cv: str, texte_offre: str,
                  competences_requises: list[str], experience_min: int) -> ResultatAnalyse:
    """Analyse un CV déjà converti en texte (cœur du pipeline, testable unitairement)."""
    competences_cv = entites.extraire_competences(texte_cv)
    requises = [c.lower() for c in competences_requises]
    trouvees = [c for c in requises if c in competences_cv]
    manquantes = [c for c in requises if c not in competences_cv]

    score_competences = len(trouvees) / len(requises) if requises else 1.0

    annees = entites.extraire_experience(texte_cv)
    score_experience = min(annees / experience_min, 1.0) if experience_min > 0 else 1.0

    score_semantique, methode = similarite_semantique(texte_cv, texte_offre)

    score_global = 100.0 * (
        POIDS_COMPETENCES * score_competences
        + POIDS_SEMANTIQUE * score_semantique
        + POIDS_EXPERIENCE * score_experience
    )

    return ResultatAnalyse(
        score_global=score_global,
        score_competences=score_competences,
        score_experience=score_experience,
        score_semantique=score_semantique,
        methode_similarite=methode,
        entites={
            "nom_candidat": entites.extraire_nom_candidat(texte_cv),
            "competences_cv": competences_cv,
            "competences_trouvees": trouvees,
            "competences_manquantes": manquantes,
            "annees_experience": annees,
            "diplomes": entites.extraire_diplomes(texte_cv),
            "contact": entites.extraire_contact(texte_cv),
        },
    )


def traiter_pdf(chemin_pdf: str, texte_offre: str,
                competences_requises: list[str], experience_min: int) -> tuple[ResultatAnalyse, str]:
    """Pipeline complet depuis un fichier PDF. Retourne (résultat, texte extrait)."""
    texte_cv = extraire_pdf(chemin_pdf)
    return traiter_texte(texte_cv, texte_offre, competences_requises, experience_min), texte_cv
