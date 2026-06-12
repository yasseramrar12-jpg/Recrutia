# Plan d'issues GitHub — Projet RECRUT'IA

À copier dans GitHub Issues (ou importer via `gh issue create`). Étiquettes suggérées :
`backend` `frontend` `ia` `bdd` `tests` `doc` · `itération-1` `itération-2` `itération-3`
· assignation : **E1** (Web & API) / **E2** (IA).

Chaque issue suit le format : objectif, critères d'acceptation, branche.

---

## Itération 1 — Fondations

**#1 — Initialiser le dépôt et la structure du projet** · E1+E2 · `doc`
Mettre en place `backend/`, `frontend/`, `.gitignore`, README, branches `main`/`develop`, protection de `main` (PR obligatoire).
✅ Le dépôt compile à vide ; la stratégie de branches est documentée dans le README.
Branche : `feature/initialisation`

**#2 — Modèle de données et connexion SQLAlchemy** · E1 · `backend` `bdd`
Implémenter `models.py` (Utilisateur, OffreEmploi, CV, Analyse) conformément au diagramme de classes du dossier.
✅ `Base.metadata.create_all` crée les 4 tables ; relations navigables dans les deux sens.
Branche : `feature/modeles`

**#3 — Authentification JWT** · E1 · `backend`
`POST /api/auth/login`, hachage PBKDF2, dépendance `utilisateur_courant`, script `seed.py`.
✅ Identifiants invalides → 401 ; toutes les routes métier exigent un jeton ; test automatisé.
Branche : `feature/auth`

**#4 — Extraction de texte PDF** · E2 · `ia`
`extraire_pdf()` avec pdfplumber + `normaliser()` ; exception `ErreurExtractionPDF` pour les scans.
✅ Un PDF natif retourne son texte ; un PDF sans texte lève l'exception ; tests unitaires.
Branche : `feature/extraction-texte`

**#5 — Maquettes et squelette React** · E1 · `frontend`
Vite + React, navigation 3 écrans (connexion, campagnes, campagne), client `api.js`, proxy `/api`.
✅ `npm run build` passe ; la connexion stocke le jeton et affiche la liste (vide) des campagnes.
Branche : `feature/squelette-front`

## Itération 2 — Première chaîne complète

**#6 — CRUD des campagnes** · E1 · `backend`
`GET/POST /api/offres`, `GET /api/offres/{id}` avec validation Pydantic.
✅ Création avec compétences normalisées en minuscules ; 404 si offre inconnue ; tests.
Branche : `feature/offres`

**#7 — Téléversement des CV** · E1 · `backend`
`POST /api/offres/{id}/cvs` multipart multiple ; stockage disque sous nom UUID.
✅ Fichier non PDF → 400 avec message explicite ; plusieurs fichiers acceptés en une requête.
Branche : `feature/upload-cv`

**#8 — Référentiel et extraction des compétences** · E2 · `ia`
Dictionnaire compétence canonique → synonymes ; correspondance insensible aux accents,
sans faux positifs (« java » ≠ « javascript »).
✅ Tests sur 5 compétences et 2 pièges ; référentiel ≥ 40 entrées.
Branche : `feature/competences`

**#9 — Similarité TF-IDF** · E2 · `ia`
`similarite_tfidf()` avec scikit-learn (vectorisation + cosinus).
✅ Un CV pertinent obtient une similarité supérieure à un CV hors sujet (test).
Branche : `feature/similarite-tfidf`

**#10 — Pipeline et score combiné v1** · E2 · `ia`
`traiter_texte()` : compétences + expérience (regex) + similarité → score /100 pondéré.
✅ Pondérations dans `config.py` ; résultat sérialisable ; tests du classement relatif.
Branche : `feature/pipeline-v1`

**#11 — Endpoint d'analyse et classement** · E1 · `backend`
`POST /analyser` (boucle sur les CV, gestion des PDF illisibles), `GET /classement`.
✅ Ré-analyse possible (anciennes analyses purgées) ; erreurs PDF remontées sans bloquer le lot.
Branche : `feature/analyse`

**#12 — Écrans campagne et classement** · E1 · `frontend`
Formulaire fiche de poste, upload, bouton d'analyse, tableau trié avec jauges de score.
✅ Détail par candidat (compétences trouvées/manquantes) ; états chargement/erreur visibles.
Branche : `feature/ecran-classement`

## Itération 3 — Qualité et industrialisation

**#13 — Extraction d'entités avancée** · E2 · `ia`
Expérience par plages de dates, diplômes, e-mail/téléphone, nom du candidat (spaCy si dispo).
✅ Fonctionne sans spaCy (repli) ; précision vérifiée sur le jeu annoté.
Branche : `feature/entites-avancees`

**#14 — Similarité sémantique par embeddings** · E2 · `ia`
Sentence-Transformers en option avec chargement paresseux et repli TF-IDF.
✅ L'application démarre sans la dépendance ; la méthode utilisée est tracée dans le résultat.
Branche : `feature/embeddings`

**#15 — Jeu annoté et script d'évaluation** · E2 · `ia` `tests`
Corpus ≥ 30 CV annotés, calcul précision/rappel/F1, comparaison des méthodes.
✅ `python -m evaluation.evaluer` affiche le tableau ; F1 combiné ≥ 0,80 ; erreurs analysées dans le dossier.
Branche : `feature/evaluation`

**#16 — Export CSV** · E1 · `backend` `frontend`
`GET /export` (CSV `;`) + lien dans l'écran de classement.
✅ Fichier ouvrable dans Excel/LibreOffice avec rang, scores et compétences.
Branche : `feature/export-csv`

**#17 — Tests d'intégration bout en bout** · E1 · `tests`
Scénario complet : login → offre → upload → analyse → classement → export (PDF générés par fpdf2).
✅ `pytest` vert en CI ; couverture du cas « fichier non PDF » et « sans authentification ».
Branche : `feature/tests-integration`

**#18 — Conteneurisation** · E1 · `backend` `frontend`
Dockerfiles + docker-compose (PostgreSQL, API, Nginx).
✅ `docker compose up --build` → application sur :8080, données persistées dans des volumes.
Branche : `feature/docker`

**#19 — Intégration continue GitHub Actions** · E1+E2 · `tests`
Workflow : installation, `pytest`, `npm run build` à chaque PR.
✅ Une PR avec test cassé est bloquée ; badge de statut dans le README.
Branche : `feature/ci`

**#20 — Documentation finale** · E1+E2 · `doc`
README à jour, docstrings, captures d'écran, synthèse de l'évaluation dans le dossier technique.
✅ Un lecteur externe installe et lance le projet en suivant uniquement le README.
Branche : `feature/doc-finale`
