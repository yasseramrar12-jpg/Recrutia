"""Calcul de similarité entre un CV et une fiche de poste.

Deux méthodes (cf. dossier technique) :
  1. TF-IDF + similarité cosinus (scikit-learn) — toujours disponible ;
  2. embeddings de phrases (Sentence-Transformers) — optionnelle, activée
     automatiquement si la bibliothèque et le modèle sont installés.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .extracteur_texte import normaliser

_modele_transformer = None
_transformer_disponible = None


def _charger_transformer():
    """Charge paresseusement le modèle Sentence-Transformers (une seule fois)."""
    global _modele_transformer, _transformer_disponible
    if _transformer_disponible is not None:
        return _modele_transformer
    try:
        from sentence_transformers import SentenceTransformer

        _modele_transformer = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )
        _transformer_disponible = True
    except Exception:
        _modele_transformer = None
        _transformer_disponible = False
    return _modele_transformer


def similarite_tfidf(texte_cv: str, texte_offre: str) -> float:
    """Similarité cosinus entre vecteurs TF-IDF (0.0 à 1.0)."""
    vectoriseur = TfidfVectorizer()
    vecteurs = vectoriseur.fit_transform([normaliser(texte_cv), normaliser(texte_offre)])
    return float(cosine_similarity(vecteurs[0], vecteurs[1])[0][0])


def similarite_semantique(texte_cv: str, texte_offre: str) -> tuple[float, str]:
    """Retourne (score, méthode utilisée).

    Utilise les embeddings si disponibles, sinon repli sur TF-IDF afin que
    le système reste fonctionnel sans GPU ni téléchargement de modèle.
    """
    modele = _charger_transformer()
    if modele is not None:
        from sentence_transformers import util

        e1 = modele.encode(texte_cv, convert_to_tensor=True)
        e2 = modele.encode(texte_offre, convert_to_tensor=True)
        return float(util.cos_sim(e1, e2)), "embeddings"
    return similarite_tfidf(texte_cv, texte_offre), "tfidf"
