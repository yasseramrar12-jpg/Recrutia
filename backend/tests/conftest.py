"""Fixtures communes : base de données de test et CV PDF générés à la volée."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DATABASE_URL"] = "sqlite:///./test_recrutia.db"
os.environ["DOSSIER_CVS"] = "test_stockage_cvs"

import pytest
from fastapi.testclient import TestClient
from fpdf import FPDF

from app.database import Base, SessionLocale, engine
from app.main import app
from app.models import Utilisateur
from app.securite import hacher_mot_de_passe

CV_PERTINENT = """Martin Dupont
Développeur Full-Stack
Email : martin.dupont@mail.fr - Tél : 06 12 34 56 78

5 ans d'expérience en développement web.

EXPÉRIENCE
2021 - 2024 : Développeur Python / React chez WebCorp
2019 - 2021 : Développeur JavaScript chez StartIt

COMPÉTENCES : Python, React, SQL, Git, Docker, FastAPI

FORMATION
Master Informatique - Université de Lyon
"""

CV_HORS_SUJET = """Claire Morel
Responsable communication

EXPÉRIENCE
2022 - 2024 : Chargée de communication, agence Pixel
Rédaction de communiqués de presse, gestion des réseaux sociaux.

FORMATION
Licence Information-Communication
"""


def _pdf_depuis_texte(texte: str, chemin: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for ligne in texte.splitlines():
        pdf.cell(0, 8, ligne.encode("latin-1", "replace").decode("latin-1"),
                 new_x="LMARGIN", new_y="NEXT")
    pdf.output(chemin)


@pytest.fixture(scope="session")
def dossier_pdfs(tmp_path_factory):
    dossier = tmp_path_factory.mktemp("cvs")
    _pdf_depuis_texte(CV_PERTINENT, str(dossier / "cv_pertinent.pdf"))
    _pdf_depuis_texte(CV_HORS_SUJET, str(dossier / "cv_hors_sujet.pdf"))
    return dossier


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocale()
    db.add(Utilisateur(nom="Test RH", email="test@demo.fr",
                       mot_de_passe_hash=hacher_mot_de_passe("test1234")))
    db.commit()
    db.close()
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def entetes(client):
    reponse = client.post("/api/auth/login",
                          json={"email": "test@demo.fr", "mot_de_passe": "test1234"})
    assert reponse.status_code == 200
    return {"Authorization": f"Bearer {reponse.json()['jeton']}"}
