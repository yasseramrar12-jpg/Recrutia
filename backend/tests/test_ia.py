"""Tests unitaires du module IA (extraction d'entités, similarité, scoring)."""
from app.ia.extracteur_entites import (extraire_competences, extraire_contact,
                                       extraire_diplomes, extraire_experience)
from app.ia.pipeline import traiter_texte
from app.ia.similarite import similarite_tfidf
from conftest import CV_HORS_SUJET, CV_PERTINENT


def test_extraction_competences():
    competences = extraire_competences(CV_PERTINENT)
    for attendue in ["python", "react", "sql", "git", "docker", "fastapi"]:
        assert attendue in competences
    assert "java" not in competences  # « JavaScript » ne doit pas matcher « java »


def test_extraction_experience_explicite():
    assert extraire_experience(CV_PERTINENT) == 5  # mention « 5 ans d'expérience »


def test_extraction_experience_plages_de_dates():
    assert extraire_experience(CV_HORS_SUJET) == 2  # 2022 - 2024


def test_extraction_contact_et_diplomes():
    contact = extraire_contact(CV_PERTINENT)
    assert contact["email"] == "martin.dupont@mail.fr"
    assert contact["telephone"] is not None
    assert "master" in extraire_diplomes(CV_PERTINENT)


def test_similarite_ordonne_les_candidats():
    offre = "Développeur web Python React SQL, API REST, Git."
    assert similarite_tfidf(CV_PERTINENT, offre) > similarite_tfidf(CV_HORS_SUJET, offre)


def test_score_global_pipeline():
    offre = "Développeur web full-stack Python / React. API REST, SQL, Git."
    requises, exp_min = ["python", "react", "sql", "git"], 2

    pertinent = traiter_texte(CV_PERTINENT, offre, requises, exp_min)
    hors_sujet = traiter_texte(CV_HORS_SUJET, offre, requises, exp_min)

    assert pertinent.score_competences == 1.0          # 4/4 compétences
    assert pertinent.score_experience == 1.0           # 5 ans >= 2 ans
    assert pertinent.score_global > hors_sujet.score_global
    assert hors_sujet.entites["competences_manquantes"] == requises
