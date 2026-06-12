import React, { useEffect, useState } from "react";
import { api } from "../api.js";

function Jauge({ valeur, seuil }) {
  // Jauge de score : la couleur encode la valeur, le trait vertical le seuil « retenu ».
  const teinte = valeur >= seuil ? "var(--ok)" : valeur >= seuil - 20 ? "var(--moyen)" : "var(--faible)";
  return (
    <div className="jauge" role="img" aria-label={`Score ${valeur} sur 100`}>
      <div className="jauge-remplie" style={{ width: `${valeur}%`, background: teinte }} />
      <div className="jauge-seuil" style={{ left: `${seuil}%` }} title={`Seuil retenu : ${seuil}`} />
      <span className="jauge-valeur">{valeur}</span>
    </div>
  );
}

function LigneCandidat({ analyse, seuil }) {
  const [ouvert, setOuvert] = useState(false);
  return (
    <>
      <tr className="ligne-candidat" onClick={() => setOuvert(!ouvert)}>
        <td className="nom-candidat">{analyse.candidat}</td>
        <td><Jauge valeur={analyse.score_global} seuil={seuil} /></td>
        <td>{analyse.annees_experience} an{analyse.annees_experience > 1 ? "s" : ""}</td>
        <td className="discret">{analyse.competences_trouvees.length} / {analyse.competences_trouvees.length + analyse.competences_manquantes.length} compétences</td>
      </tr>
      {ouvert && (
        <tr className="ligne-detail">
          <td colSpan={4}>
            <div className="etiquettes">
              {analyse.competences_trouvees.map((c) => <span key={c} className="etiquette ok">{c}</span>)}
              {analyse.competences_manquantes.map((c) => <span key={c} className="etiquette manque">{c}</span>)}
            </div>
            <p className="discret">
              Compétences : {(analyse.score_competences * 100).toFixed(0)} % ·
              Sémantique : {(analyse.score_semantique * 100).toFixed(0)} % ·
              Expérience : {(analyse.score_experience * 100).toFixed(0)} %
              {analyse.contact?.email && <> · {analyse.contact.email}</>}
              {analyse.diplomes?.length > 0 && <> · Diplômes : {analyse.diplomes.join(", ")}</>}
            </p>
          </td>
        </tr>
      )}
    </>
  );
}

export default function Campagne({ id, retour }) {
  const [offre, setOffre] = useState(null);
  const [classement, setClassement] = useState(null);
  const [fichiers, setFichiers] = useState([]);
  const [message, setMessage] = useState(null);
  const [erreur, setErreur] = useState(null);
  const [analyseEnCours, setAnalyseEnCours] = useState(false);

  async function charger() {
    const o = await api.detailOffre(id);
    setOffre(o);
    if (o.nb_analyses > 0) setClassement(await api.classement(id));
  }
  useEffect(() => { charger().catch((e) => setErreur(e.message)); }, [id]);

  async function televerser(evt) {
    evt.preventDefault();
    setErreur(null);
    try {
      const r = await api.televerserCVs(id, fichiers);
      setMessage(`${r.cvs_enregistres.length} CV enregistré(s).`);
      setFichiers([]);
      evt.target.reset();
      await charger();
    } catch (e) { setErreur(e.message); }
  }

  async function lancerAnalyse() {
    setErreur(null);
    setMessage(null);
    setAnalyseEnCours(true);
    try {
      const r = await api.analyser(id);
      if (r.erreurs?.length) {
        setErreur(r.erreurs.map((e) => `${e.cv} : ${e.erreur}`).join(" — "));
      }
      await charger();
    } catch (e) { setErreur(e.message); }
    finally { setAnalyseEnCours(false); }
  }

  if (offre === null) return <p className="discret">Chargement…</p>;

  return (
    <div>
      <button className="lien" onClick={retour}>← Toutes les campagnes</button>
      <div className="entete-campagne">
        <h2>{offre.titre}</h2>
        <div className="etiquettes">
          {offre.competences_requises.map((c) => <span key={c} className="etiquette">{c}</span>)}
          {offre.experience_min > 0 && <span className="etiquette">≥ {offre.experience_min} ans</span>}
        </div>
      </div>
      <p className="description">{offre.description}</p>

      <div className="deux-colonnes">
        <section className="carte">
          <h3>CV de la campagne ({offre.nb_cvs})</h3>
          <form onSubmit={televerser} className="formulaire">
            <label>
              Ajouter des CV (PDF)
              <input type="file" accept="application/pdf" multiple required
                     onChange={(e) => setFichiers(e.target.files)} />
            </label>
            <button className="secondaire">Téléverser</button>
          </form>
          {message && <p className="info">{message}</p>}
        </section>

        <section className="carte action-analyse">
          <h3>Analyse IA</h3>
          <p className="discret">
            Extraction des compétences, de l'expérience et calcul de la similarité
            sémantique avec la fiche de poste.
          </p>
          <button className="principal" onClick={lancerAnalyse}
                  disabled={offre.nb_cvs === 0 || analyseEnCours}>
            {analyseEnCours ? "Analyse en cours…" : "Lancer l'analyse"}
          </button>
        </section>
      </div>

      {erreur && <p className="erreur">{erreur}</p>}

      {classement && (
        <section className="carte resultats">
          <div className="entete-resultats">
            <h3>Classement des candidats</h3>
            <a className="lien" href={api.urlExport(id)}>Exporter en CSV</a>
          </div>
          <table>
            <thead>
              <tr><th>Candidat</th><th>Score de correspondance</th><th>Expérience</th><th>Compétences</th></tr>
            </thead>
            <tbody>
              {classement.classement.map((a) => (
                <LigneCandidat key={a.analyse_id} analyse={a} seuil={classement.seuil_retenu} />
              ))}
            </tbody>
          </table>
          <p className="discret">Cliquez sur un candidat pour le détail. Le trait vertical marque le seuil « retenu » ({classement.seuil_retenu}/100).</p>
        </section>
      )}
    </div>
  );
}
