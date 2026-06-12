import React, { useState } from "react";
import { api } from "../api.js";

export default function Connexion({ onConnecte }) {
  const [email, setEmail] = useState("rh@demo.fr");
  const [motDePasse, setMotDePasse] = useState("");
  const [erreur, setErreur] = useState(null);
  const [enCours, setEnCours] = useState(false);

  async function soumettre(evt) {
    evt.preventDefault();
    setErreur(null);
    setEnCours(true);
    try {
      await api.connexion(email, motDePasse);
      onConnecte();
    } catch (e) {
      setErreur(e.message);
    } finally {
      setEnCours(false);
    }
  }

  return (
    <div className="connexion">
      <form className="carte connexion-carte" onSubmit={soumettre}>
        <h1 className="logo grand">RECRUT<span>'IA</span></h1>
        <p className="sous-titre">Triez vos candidatures, gardez la décision.</p>
        <label>
          Adresse e-mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Mot de passe
          <input type="password" value={motDePasse} onChange={(e) => setMotDePasse(e.target.value)}
                 placeholder="demo1234" required />
        </label>
        {erreur && <p className="erreur">{erreur}</p>}
        <button className="principal" disabled={enCours}>
          {enCours ? "Connexion…" : "Se connecter"}
        </button>
      </form>
    </div>
  );
}
