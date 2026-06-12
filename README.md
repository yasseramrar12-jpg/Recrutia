# RECRUT'IA — Assistant de recrutement : analyseur de CV intelligent
[![CI](https://github.com/yasseramrar12-jpg/Recrutia/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/yasseramrar12-jpg/Recrutia/actions/workflows/ci.yml)

Projet de génie logiciel : application web permettant aux RH de téléverser des CV (PDF)
et une fiche de poste ; l'IA (NLP) note la correspondance et classe les candidats.
Voir le **dossier technique** pour la modélisation UML complète.

## Architecture

| Module | Technologie | Dossier |
|---|---|---|
| Web-RECRUT (frontend) | React + Vite | `frontend/` |
| API-RECRUT (backend) | Python / FastAPI / SQLAlchemy | `backend/app/` |
| IA-RECRUT (pipeline NLP) | pdfplumber, scikit-learn, (option) spaCy & Sentence-Transformers | `backend/app/ia/` |
| Base de données | SQLite en développement, PostgreSQL en production (`DATABASE_URL`) | — |

## Démarrage rapide

### 1. Backend (terminal 1)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python seed.py            # crée le compte de démonstration rh@demo.fr / demo1234
uvicorn app.main:app --reload
```

API disponible sur http://localhost:8000 — documentation interactive sur http://localhost:8000/docs

### 2. Frontend (terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Application sur http://localhost:5173 (le proxy Vite redirige `/api` vers le backend).

### 3. Tests

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

Les tests génèrent eux-mêmes des CV PDF (fpdf2) : aucun fichier externe n'est requis.

## Options IA (recommandées en itération 3)

Le système fonctionne sans ces dépendances (repli automatique sur TF-IDF), mais
la qualité augmente avec :

```bash
pip install sentence-transformers          # similarité sémantique par embeddings
pip install spacy && python -m spacy download fr_core_news_md   # nom du candidat (entités PER)
```

## Variables d'environnement

| Variable | Défaut | Rôle |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./recrutia.db` | ex. `postgresql+psycopg://user:mdp@localhost/recrutia` |
| `SECRET_JWT` | clé de développement | **à changer en production** |
| `DOSSIER_CVS` | `stockage_cvs` | stockage des PDF téléversés |

## Score de correspondance

`score = 100 × (0,5 × compétences + 0,3 × similarité_sémantique + 0,2 × expérience)`
— pondérations dans `backend/app/config.py`, seuil « retenu » à 60/100.

## Évaluation du modèle

Un jeu de 38 CV annotés (`backend/evaluation/jeu_donnees.py`) permet de mesurer
précision, rappel et F1 du scoring, et de comparer les méthodes :

```bash
cd backend
python -m evaluation.evaluer
```

Résultat attendu : F1 ≈ 0,95 pour le score combiné (le script échoue sous 0,80,
ce qui en fait un garde-fou en intégration continue). Les erreurs résiduelles
sont listées pour alimenter l'analyse des limites dans le dossier technique.

## Démarrage avec Docker (pile complète PostgreSQL)

```bash
docker compose up --build
```

Application sur http://localhost:8080, API et documentation sur http://localhost:8000/docs.
Les CV et la base sont persistés dans des volumes Docker.

## Plan de travail

Le découpage en 20 issues sur 3 itérations (avec critères d'acceptation et
branches) est dans [`PLAN_ISSUES.md`](PLAN_ISSUES.md). L'intégration continue
(`.github/workflows/ci.yml`) rejoue tests, évaluation et compilation à chaque
pull request.

## Organisation Git

Branches `main` (stable) / `develop` (intégration) / `feature/<nom>` ; commits
`type(portée): description` ; fusion par pull request relue.
