"""Configuration de l'application RECRUT'IA."""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recrutia.db")
SECRET_JWT = os.getenv("SECRET_JWT", "cle-de-developpement-a-changer-en-production-0123456789")
DUREE_JETON_MINUTES = int(os.getenv("DUREE_JETON_MINUTES", "480"))
DOSSIER_CVS = os.getenv("DOSSIER_CVS", "stockage_cvs")

# Pondérations du score global (paramétrables)
POIDS_COMPETENCES = 0.5
POIDS_SEMANTIQUE = 0.3
POIDS_EXPERIENCE = 0.2
SEUIL_RETENU = 60.0
