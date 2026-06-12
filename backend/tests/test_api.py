"""Tests d'intégration de l'API (scénario complet du diagramme de séquence)."""


def _creer_offre(client, entetes):
    reponse = client.post("/api/offres", headers=entetes, json={
        "titre": "Développeur Web Full-Stack",
        "description": "Nous recherchons un développeur maîtrisant Python, React et SQL "
                       "pour concevoir des API REST.",
        "competences_requises": ["python", "react", "sql", "git"],
        "experience_min": 2,
    })
    assert reponse.status_code == 201
    return reponse.json()["id"]


def test_authentification_requise(client):
    assert client.get("/api/offres").status_code == 401


def test_identifiants_invalides(client):
    r = client.post("/api/auth/login", json={"email": "test@demo.fr", "mot_de_passe": "faux"})
    assert r.status_code == 401


def test_fichier_non_pdf_rejete(client, entetes):
    offre_id = _creer_offre(client, entetes)
    r = client.post(f"/api/offres/{offre_id}/cvs", headers=entetes,
                    files=[("fichiers", ("cv.txt", b"bonjour", "text/plain"))])
    assert r.status_code == 400


def test_scenario_complet(client, entetes, dossier_pdfs):
    """Création d'offre -> téléversement -> analyse -> classement -> export CSV."""
    offre_id = _creer_offre(client, entetes)

    fichiers = [
        ("fichiers", ("cv_pertinent.pdf", (dossier_pdfs / "cv_pertinent.pdf").read_bytes(), "application/pdf")),
        ("fichiers", ("cv_hors_sujet.pdf", (dossier_pdfs / "cv_hors_sujet.pdf").read_bytes(), "application/pdf")),
    ]
    r = client.post(f"/api/offres/{offre_id}/cvs", headers=entetes, files=fichiers)
    assert r.status_code == 201 and r.json()["nb_cvs"] == 2

    r = client.post(f"/api/offres/{offre_id}/analyser", headers=entetes)
    assert r.status_code == 200 and r.json()["nb_analyses"] == 2

    r = client.get(f"/api/offres/{offre_id}/classement", headers=entetes)
    assert r.status_code == 200
    classement = r.json()["classement"]
    assert len(classement) == 2
    assert classement[0]["score_global"] >= classement[1]["score_global"]
    assert "python" in classement[0]["competences_trouvees"]

    detail = client.get(f"/api/analyses/{classement[0]['analyse_id']}", headers=entetes)
    assert detail.status_code == 200

    export = client.get(f"/api/offres/{offre_id}/export", headers=entetes)
    assert export.status_code == 200
    assert "rang;candidat" in export.text.splitlines()[0]
