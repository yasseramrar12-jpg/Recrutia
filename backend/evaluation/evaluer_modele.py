"""Évaluation du modèle de scoring (cf. section « Évaluation » du dossier technique).

Compare trois variantes sur le jeu annoté :
  - similarité TF-IDF seule (seuillée) ;
  - score compétences seul ;
  - score combiné (modèle retenu : 0,5 / 0,3 / 0,2).

Usage :  python -m evaluation.evaluer_modele  (depuis backend/)
"""
import sys

from sklearn.metrics import f1_score, precision_score, recall_score

from app.config import SEUIL_RETENU
from app.ia.pipeline import traiter_texte
from app.ia.similarite import similarite_tfidf

from .jeu_donnees import OFFRES, generer_jeu


def _texte_offre(offre: dict) -> str:
    return f"{offre['titre']}. {offre['description']}. " + " ".join(offre["competences_requises"])


def evaluer(seuil: float = SEUIL_RETENU) -> dict:
    exemples = generer_jeu()
    labels, scores_combines, scores_tfidf, scores_competences = [], [], [], []

    for exemple in exemples:
        offre = OFFRES[exemple["offre"]]
        resultat = traiter_texte(
            exemple["texte_cv"], _texte_offre(offre),
            offre["competences_requises"], offre["experience_min"],
        )
        labels.append(exemple["label"])
        scores_combines.append(resultat.score_global)
        scores_competences.append(100 * resultat.score_competences)
        scores_tfidf.append(100 * similarite_tfidf(exemple["texte_cv"], _texte_offre(offre)))

    variantes = {
        "TF-IDF seul (seuil 25)": [s >= 25 for s in scores_tfidf],
        "Compétences seules (seuil 75)": [s >= 75 for s in scores_competences],
        f"Score combiné (seuil {seuil:.0f})": [s >= seuil for s in scores_combines],
    }

    resultats = {}
    for nom, predictions in variantes.items():
        resultats[nom] = {
            "precision": precision_score(labels, predictions, zero_division=0),
            "rappel": recall_score(labels, predictions, zero_division=0),
            "f1": f1_score(labels, predictions, zero_division=0),
        }
    return resultats, labels, scores_combines


def meilleur_seuil(labels: list[int], scores: list[float]) -> tuple[float, float]:
    """Balaye les seuils de 30 à 90 et retourne (seuil, F1) optimal."""
    meilleur = (0.0, 0.0)
    for seuil in range(30, 91, 5):
        f1 = f1_score(labels, [s >= seuil for s in scores], zero_division=0)
        if f1 > meilleur[1]:
            meilleur = (float(seuil), f1)
    return meilleur


if __name__ == "__main__":
    resultats, labels, scores = evaluer()
    print(f"Jeu d'évaluation : {len(labels)} CV annotés "
          f"({sum(labels)} pertinents / {len(labels) - sum(labels)} non pertinents)\n")
    print(f"{'Variante':<34}{'Précision':>10}{'Rappel':>10}{'F1':>8}")
    print("-" * 62)
    for nom, m in resultats.items():
        print(f"{nom:<34}{m['precision']:>10.2f}{m['rappel']:>10.2f}{m['f1']:>8.2f}")
    seuil, f1 = meilleur_seuil(labels, scores)
    print(f"\nSeuil optimal pour le score combiné : {seuil:.0f}/100 (F1 = {f1:.2f})")
    nom_combine = [n for n in resultats if n.startswith("Score combiné")][0]
    sys.exit(0 if resultats[nom_combine]["f1"] >= 0.80 else 1)
