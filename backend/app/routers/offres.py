"""Gestion des campagnes de recrutement et des CV."""
import csv
import io
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import DOSSIER_CVS, SEUIL_RETENU
from ..database import get_db
from ..deps import utilisateur_courant
from ..ia.extracteur_texte import ErreurExtractionPDF
from ..ia.pipeline import traiter_pdf
from ..models import CV, Analyse, OffreEmploi, Utilisateur
from ..schemas import OffreCreation, OffreReponse

router = APIRouter(prefix="/api/offres", tags=["Offres"])


def _vers_reponse(offre: OffreEmploi) -> OffreReponse:
    return OffreReponse(
        id=offre.id, titre=offre.titre, description=offre.description,
        competences_requises=offre.competences_requises or [],
        experience_min=offre.experience_min,
        nb_cvs=len(offre.cvs), nb_analyses=len(offre.analyses),
    )


def _offre_ou_404(offre_id: int, db: Session) -> OffreEmploi:
    offre = db.get(OffreEmploi, offre_id)
    if offre is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Offre inconnue")
    return offre


@router.get("", response_model=list[OffreReponse])
def lister_offres(db: Session = Depends(get_db),
                  user: Utilisateur = Depends(utilisateur_courant)):
    offres = db.scalars(select(OffreEmploi).order_by(OffreEmploi.date_creation.desc())).all()
    return [_vers_reponse(o) for o in offres]


@router.post("", response_model=OffreReponse, status_code=status.HTTP_201_CREATED)
def creer_offre(requete: OffreCreation, db: Session = Depends(get_db),
                user: Utilisateur = Depends(utilisateur_courant)):
    offre = OffreEmploi(
        utilisateur_id=user.id, titre=requete.titre, description=requete.description,
        competences_requises=[c.strip().lower() for c in requete.competences_requises if c.strip()],
        experience_min=requete.experience_min,
    )
    db.add(offre)
    db.commit()
    db.refresh(offre)
    return _vers_reponse(offre)


@router.get("/{offre_id}", response_model=OffreReponse)
def detail_offre(offre_id: int, db: Session = Depends(get_db),
                 user: Utilisateur = Depends(utilisateur_courant)):
    return _vers_reponse(_offre_ou_404(offre_id, db))


@router.post("/{offre_id}/cvs", status_code=status.HTTP_201_CREATED)
def televerser_cvs(offre_id: int, fichiers: list[UploadFile],
                   db: Session = Depends(get_db),
                   user: Utilisateur = Depends(utilisateur_courant)):
    """Téléverse un ou plusieurs CV PDF (multipart/form-data, champ « fichiers »)."""
    offre = _offre_ou_404(offre_id, db)
    os.makedirs(DOSSIER_CVS, exist_ok=True)
    enregistres = []
    for fichier in fichiers:
        if not (fichier.filename or "").lower().endswith(".pdf"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"« {fichier.filename} » n'est pas un PDF. Seul le format PDF est accepté.",
            )
        chemin = os.path.join(DOSSIER_CVS, f"{uuid.uuid4().hex}.pdf")
        with open(chemin, "wb") as sortie:
            sortie.write(fichier.file.read())
        cv = CV(offre_id=offre.id, nom_fichier=fichier.filename, chemin_fichier=chemin)
        db.add(cv)
        enregistres.append(fichier.filename)
    db.commit()
    return {"offre_id": offre.id, "cvs_enregistres": enregistres, "nb_cvs": len(offre.cvs)}


@router.post("/{offre_id}/analyser")
def analyser_offre(offre_id: int, db: Session = Depends(get_db),
                   user: Utilisateur = Depends(utilisateur_courant)):
    """Lance l'analyse IA de tous les CV de la campagne (cf. diagramme de séquence)."""
    offre = _offre_ou_404(offre_id, db)
    if not offre.cvs:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Aucun CV à analyser pour cette offre")

    # On repart d'analyses propres si l'offre a déjà été analysée.
    for ancienne in list(offre.analyses):
        db.delete(ancienne)

    erreurs = []
    for cv in offre.cvs:
        try:
            resultat, texte = traiter_pdf(
                cv.chemin_fichier, offre.get_texte_complet(),
                offre.competences_requises or [], offre.experience_min,
            )
        except ErreurExtractionPDF as exc:
            erreurs.append({"cv": cv.nom_fichier, "erreur": str(exc)})
            continue
        cv.texte_extrait = texte
        db.add(Analyse(
            cv_id=cv.id, offre_id=offre.id,
            score_global=resultat.score_global,
            score_competences=resultat.score_competences,
            score_experience=resultat.score_experience,
            score_semantique=resultat.score_semantique,
            entites=resultat.entites,
        ))
    db.commit()
    db.refresh(offre)
    return {
        "offre_id": offre.id,
        "nb_analyses": len(offre.analyses),
        "erreurs": erreurs,
        "methode_similarite": "embeddings ou tfidf selon installation",
    }


@router.get("/{offre_id}/classement")
def classement(offre_id: int, db: Session = Depends(get_db),
               user: Utilisateur = Depends(utilisateur_courant)):
    offre = _offre_ou_404(offre_id, db)
    analyses = sorted(offre.analyses, key=lambda a: a.score_global, reverse=True)
    return {
        "offre_id": offre.id,
        "titre": offre.titre,
        "seuil_retenu": SEUIL_RETENU,
        "classement": [a.to_dict() for a in analyses],
    }


@router.get("/{offre_id}/export")
def exporter_csv(offre_id: int, db: Session = Depends(get_db),
                 user: Utilisateur = Depends(utilisateur_courant)):
    offre = _offre_ou_404(offre_id, db)
    analyses = sorted(offre.analyses, key=lambda a: a.score_global, reverse=True)
    tampon = io.StringIO()
    champs = ["rang", "candidat", "score_global", "score_competences",
              "score_semantique", "score_experience", "annees_experience",
              "competences_trouvees", "competences_manquantes"]
    ecrivain = csv.DictWriter(tampon, fieldnames=champs, delimiter=";")
    ecrivain.writeheader()
    for rang, analyse in enumerate(analyses, start=1):
        ligne = analyse.to_dict()
        ecrivain.writerow({
            "rang": rang,
            "candidat": ligne["candidat"],
            "score_global": ligne["score_global"],
            "score_competences": ligne["score_competences"],
            "score_semantique": ligne["score_semantique"],
            "score_experience": ligne["score_experience"],
            "annees_experience": ligne["annees_experience"],
            "competences_trouvees": ", ".join(ligne["competences_trouvees"]),
            "competences_manquantes": ", ".join(ligne["competences_manquantes"]),
        })
    tampon.seek(0)
    return StreamingResponse(
        iter([tampon.getvalue()]), media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=classement_offre_{offre.id}.csv"},
    )
