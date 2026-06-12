"""Initialise la base avec un compte de démonstration.

Usage : python seed.py
Compte créé : rh@demo.fr / demo1234
"""
from app.database import Base, SessionLocale, engine
from app.models import Utilisateur
from app.securite import hacher_mot_de_passe

Base.metadata.create_all(bind=engine)
db = SessionLocale()
if db.query(Utilisateur).filter_by(email="rh@demo.fr").first() is None:
    db.add(Utilisateur(nom="Compte Démo RH", email="rh@demo.fr",
                       mot_de_passe_hash=hacher_mot_de_passe("demo1234"), role="RH"))
    db.commit()
    print("Compte créé : rh@demo.fr / demo1234")
else:
    print("Le compte de démonstration existe déjà.")
db.close()
