import React, { useState } from "react";
import { deconnecter, jeton } from "./api.js";
import Campagne from "./pages/Campagne.jsx";
import Campagnes from "./pages/Campagnes.jsx";
import Connexion from "./pages/Connexion.jsx";

// Navigation par état (simple et lisible pour le projet) :
// { nom: "campagnes" } ou { nom: "campagne", id: 12 }
export default function App() {
  const [connecte, setConnecte] = useState(Boolean(jeton()));
  const [vue, setVue] = useState({ nom: "campagnes" });

  if (!connecte) return <Connexion onConnecte={() => setConnecte(true)} />;

  return (
    <div className="app">
      <header className="barre">
        <button className="logo" onClick={() => setVue({ nom: "campagnes" })}>
          RECRUT<span>'IA</span>
        </button>
        <div className="barre-droite">
          <span className="utilisateur">{localStorage.getItem("nom")}</span>
          <button className="lien" onClick={() => { deconnecter(); setConnecte(false); }}>
            Se déconnecter
          </button>
        </div>
      </header>
      <main>
        {vue.nom === "campagnes" && (
          <Campagnes ouvrirCampagne={(id) => setVue({ nom: "campagne", id })} />
        )}
        {vue.nom === "campagne" && (
          <Campagne id={vue.id} retour={() => setVue({ nom: "campagnes" })} />
        )}
      </main>
    </div>
  );
}
