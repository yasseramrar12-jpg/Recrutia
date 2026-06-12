"""Évaluation du modèle de scoring sur le jeu de CV annotés.

Usage :  python -m evaluation.evaluer            (depuis backend/)

Compare trois prédicteurs au même seuil de décision :
  - similarité seule (le score sémantique décide) ;
  - compétences seules (la couverture du référentiel décide) ;
  - score combiné (pondérations du projet : 0,5 / 0,3 / 0,2).

Métriques : précision, rappel, F1 (classe positive = « candidat pertinent »).
"""
import sys

from app.config import SEUIL_RETENU
from app.ia.pipeline import traiter_texte

from .jeu_donnees import CORPUS, OFFRES


def metriques(predictions: list[bool], verites: list[bool]) -> dict:
    vp = sum(1 for p, v in zip(predictions, verites) if p and v)
    fp = sum(1 for p, v in zip(predictions, verites) if p and not v)
    fn = sum(1 for p, v in zip(predictions, verites) if not p and v)
    precision = vp / (vp + fp) if (vp + fp) else 0.0
    rappel = vp / (vp + fn) if (vp + fn) else 0.0
    f1 = 2 * precision * rappel / (precision + rappel) if (precision + rappel) else 0.0
    return {"precision": precision, "rappel": rappel, "f1": f1}


def evaluer():
    verites, resultats = [], []
    for cle_offre, pertinent, texte_cv in CORPUS:
        offre = OFFRES[cle_offre]
        texte_offre = f"{offre['titre']}. {offre['description']} " + " ".join(offre["competences_requises"])
        resultat = traiter_texte(texte_cv, texte_offre,
                                 offre["competences_requises"], offre["experience_min"])
        verites.append(pertinent)
        resultats.append(resultat)

    predicteurs = {
        "Similarité seule": [r.score_semantique * 100 >= SEUIL_RETENU * 0.5 for r in resultats],
        "Compétences seules": [r.score_competences * 100 >= SEUIL_RETENU for r in resultats],
        "Score combiné (projet)": [r.score_global >= SEUIL_RETENU for r in resultats],
    }

    largeur = max(len(n) for n in predicteurs)
    print(f"\nÉvaluation sur {len(CORPUS)} CV annotés "
          f"({sum(verites)} pertinents / {len(verites) - sum(verites)} non pertinents) "
          f"— seuil retenu : {SEUIL_RETENU:.0f}/100\n")
    print(f"{'Méthode'.ljust(largeur)}   Précision   Rappel   F1")
    print("-" * (largeur + 32))
    scores_f1 = {}
    for nom, predictions in predicteurs.items():
        m = metriques(predictions, verites)
        scores_f1[nom] = m["f1"]
        print(f"{nom.ljust(largeur)}   {m['precision']:9.2f}   {m['rappel']:6.2f}   {m['f1']:4.2f}")

    erreurs = [(CORPUS[i][0], CORPUS[i][2].splitlines()[0], resultats[i].score_global, verites[i])
               for i, p in enumerate(predicteurs["Score combiné (projet)"]) if p != verites[i]]
    if erreurs:
        print("\nErreurs du score combiné :")
        for offre, nom, score, verite in erreurs:
            attendu = "pertinent" if verite else "non pertinent"
            print(f"  - [{offre}] {nom} : score {score:.1f} (attendu : {attendu})")
    else:
        print("\nAucune erreur du score combiné sur ce jeu.")

    # Critère de validation du dossier technique : F1 >= 0,80
    return 0 if scores_f1["Score combiné (projet)"] >= 0.80 else 1


if __name__ == "__main__":
    sys.exit(evaluer())
