"""Modèles de données (cf. diagramme de classes du dossier technique)."""
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="RH")

    offres: Mapped[list["OffreEmploi"]] = relationship(back_populates="auteur")


class OffreEmploi(Base):
    __tablename__ = "offre_emploi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    utilisateur_id: Mapped[int] = mapped_column(ForeignKey("utilisateur.id"))
    titre: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    competences_requises: Mapped[list] = mapped_column(JSON, default=list)
    experience_min: Mapped[int] = mapped_column(Integer, default=0)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    auteur: Mapped["Utilisateur"] = relationship(back_populates="offres")
    cvs: Mapped[list["CV"]] = relationship(back_populates="offre", cascade="all, delete-orphan")
    analyses: Mapped[list["Analyse"]] = relationship(back_populates="offre", cascade="all, delete-orphan")

    def get_texte_complet(self) -> str:
        """Texte utilisé pour la similarité sémantique."""
        return f"{self.titre}. {self.description}. " + " ".join(self.competences_requises or [])


class CV(Base):
    __tablename__ = "cv"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offre_id: Mapped[int] = mapped_column(ForeignKey("offre_emploi.id"))
    nom_fichier: Mapped[str] = mapped_column(String(255))
    chemin_fichier: Mapped[str] = mapped_column(String(255))
    texte_extrait: Mapped[str] = mapped_column(Text, default="")
    date_depot: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    offre: Mapped["OffreEmploi"] = relationship(back_populates="cvs")
    analyses: Mapped[list["Analyse"]] = relationship(back_populates="cv", cascade="all, delete-orphan")


class Analyse(Base):
    __tablename__ = "analyse"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cv_id: Mapped[int] = mapped_column(ForeignKey("cv.id"))
    offre_id: Mapped[int] = mapped_column(ForeignKey("offre_emploi.id"))
    score_global: Mapped[float] = mapped_column(Float, default=0.0)
    score_competences: Mapped[float] = mapped_column(Float, default=0.0)
    score_experience: Mapped[float] = mapped_column(Float, default=0.0)
    score_semantique: Mapped[float] = mapped_column(Float, default=0.0)
    entites: Mapped[dict] = mapped_column(JSON, default=dict)
    date_analyse: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cv: Mapped["CV"] = relationship(back_populates="analyses")
    offre: Mapped["OffreEmploi"] = relationship(back_populates="analyses")

    def to_dict(self) -> dict:
        ent = self.entites or {}
        return {
            "analyse_id": self.id,
            "cv_id": self.cv_id,
            "nom_fichier": self.cv.nom_fichier if self.cv else None,
            "candidat": ent.get("nom_candidat") or (self.cv.nom_fichier if self.cv else "?"),
            "score_global": round(self.score_global, 1),
            "score_competences": round(self.score_competences, 3),
            "score_semantique": round(self.score_semantique, 3),
            "score_experience": round(self.score_experience, 3),
            "competences_trouvees": ent.get("competences_trouvees", []),
            "competences_manquantes": ent.get("competences_manquantes", []),
            "annees_experience": ent.get("annees_experience", 0),
            "diplomes": ent.get("diplomes", []),
            "contact": ent.get("contact", {}),
        }
