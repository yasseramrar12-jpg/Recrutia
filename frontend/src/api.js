// Client HTTP minimal : ajoute le jeton JWT et gère les erreurs de l'API.

export function jeton() {
  return localStorage.getItem("jeton");
}

export function deconnecter() {
  localStorage.removeItem("jeton");
  localStorage.removeItem("nom");
}
const BASE_URL = "";

async function requete(chemin, options = {}) {
  const entetes = { ...(options.headers || {}) };
  if (jeton()) entetes["Authorization"] = `Bearer ${jeton()}`;
  if (options.json !== undefined) {
    entetes["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.json);
  }
  const reponse = await fetch(`${BASE_URL}${chemin}`, { ...options, headers: entetes });

  if (!reponse.ok) {
    let detail = `Erreur ${reponse.status}`;
    try {
      const corps = await reponse.json();
      if (corps.detail) detail = typeof corps.detail === "string" ? corps.detail : JSON.stringify(corps.detail);
    } catch { /* corps non JSON */ }
    throw new Error(detail);
  }
  return reponse;
}

export const api = {
  async connexion(email, mot_de_passe) {
    const r = await requete("/api/auth/login", { method: "POST", json: { email, mot_de_passe } });
    const donnees = await r.json();
    localStorage.setItem("jeton", donnees.jeton);
    localStorage.setItem("nom", donnees.nom);
    return donnees;
  },
  listerOffres: () => requete("/api/offres").then(r => r.json()),
  creerOffre: (offre) => requete("/api/offres", { method: "POST", json: offre }).then(r => r.json()),
  detailOffre: (id) => requete(`/api/offres/${id}`).then(r => r.json()),
  televerserCVs(id, fichiers) {
    const formulaire = new FormData();
    [...fichiers].forEach(f => formulaire.append("fichiers", f));
    return requete(`/api/offres/${id}/cvs`, { method: "POST", body: formulaire }).then(r => r.json());
  },
  analyser: (id) => requete(`/api/offres/${id}/analyser`, { method: "POST" }).then(r => r.json()),
  classement: (id) => requete(`/api/offres/${id}/classement`).then(r => r.json()),
  urlExport: (id) => `/api/offres/${id}/export`,
};
