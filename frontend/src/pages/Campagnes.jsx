import React, { useEffect, useState } from "react";
import { api } from "../api.js";

const FORMULAIRE_VIDE = { titre: "", description: "", competences: "", experience_min: 0 };

export default function Campagnes({ ouvrirCampagne }) {
  const [offres, setOffres] = useState(null);
  const [formulaire, setFormulaire] = useState(FORMULAIRE_VIDE);
  const [erreur, setErreur] = useState(null);

  const charger = () => api.listerOffres().then(setOffres).catch((e) => setErreur(e.message));
  useEffect(() => { charger(); }, []);

  async function creer(evt) {
    evt.preventDefault();
    setErreur(null);
    try {
      const offre = await api.creerOffre({
        titre: formulaire.titre,
        description: formulaire.description,
        competences_requises: formulaire.competences.split(",").map((c) => c.trim()).filter(Boolean),
        experience_min: Number(formulaire.experience_min),
      });
      setFormulaire(FORMULAIRE_VIDE);
      ouvrirCampagne(offre.id);
    } catch (e) {
      setErreur(e.message);
    }
  }

  return (
    <div className="deux-colonnes">
      <section>
        <h2>Campagnes de recrutement</h2>
        {offres === null && <p className="discret">Chargement…</p>}
        {offres?.length === 0 && (
          <p className="discret">Aucune campagne pour l'instant. Créez la première ci-contre.</p>
        )}
        <ul className="liste-campagnes">
          {offres?.map((o) => (
            <li key={o.id}>
              <button className="carte campagne" onClick={() => ouvrirCampagne(o.id)}>
                <strong>{o.titre}</strong>
                <span className="discret">
                  {o.nb_cvs} CV · {o.nb_analyses > 0 ? "analysée" : "en attente d'analyse"}
                </span>
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section className="carte">
        <h2>Nouvelle campagne</h2>
        <form onSubmit={creer} className="formulaire">
          <label>
            Intitulé du poste
            <input value={formulaire.titre} required minLength={3}
                   onChange={(e) => setFormulaire({ ...formulaire, titre: e.target.value })} />
          </label>
          <label>
            Fiche de poste
            <textarea rows={6} value={formulaire.description} required minLength={10}
                      placeholder="Missions, contexte, profil recherché…"
                      onChange={(e) => setFormulaire({ ...formulaire, description: e.target.value })} />
          </label>
          <label>
            Compétences requises <span className="discret">(séparées par des virgules)</span>
            <input value={formulaire.competences} placeholder="python, react, sql, git"
                   onChange={(e) => setFormulaire({ ...formulaire, competences: e.target.value })} />
          </label>
          <label>
            Expérience minimale (années)
            <input type="number" min={0} max={40} value={formulaire.experience_min}
                   onChange={(e) => setFormulaire({ ...formulaire, experience_min: e.target.value })} />
          </label>
          {erreur && <p className="erreur">{erreur}</p>}
          <button className="principal">Créer la campagne</button>
        </form>
      </section>
    </div>
  );
}
