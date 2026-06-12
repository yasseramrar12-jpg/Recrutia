"""Jeu de données annoté pour l'évaluation du modèle de scoring.

30 CV synthétiques (mais réalistes) répartis sur 3 fiches de poste.
Chaque CV porte une étiquette « pertinent » attribuée à la construction :
c'est la vérité terrain à laquelle on compare les prédictions du pipeline.

Le corpus est volontairement difficile : certains profils non pertinents
partagent du vocabulaire avec l'offre (ex. un commercial « secteur IT »).
"""

OFFRES = {
    "dev_web": {
        "titre": "Développeur Web Full-Stack",
        "description": "Conception et développement d'applications web : API REST en Python, "
                       "interfaces React, bases de données relationnelles. Travail en équipe "
                       "agile avec intégration continue.",
        "competences_requises": ["python", "react", "sql", "git"],
        "experience_min": 2,
    },
    "data_analyst": {
        "titre": "Data Analyst",
        "description": "Analyse de données métier : nettoyage et préparation des données, "
                       "tableaux de bord, requêtes SQL, automatisation en Python avec pandas. "
                       "Restitution des résultats aux équipes métier.",
        "competences_requises": ["python", "sql", "pandas", "excel"],
        "experience_min": 1,
    },
    "tech_reseau": {
        "titre": "Technicien Réseaux et Systèmes",
        "description": "Administration des réseaux d'entreprise : équipements Cisco, "
                       "serveurs Linux et Windows Server, virtualisation, supervision "
                       "et support utilisateurs.",
        "competences_requises": ["tcp/ip", "cisco", "linux", "windows server"],
        "experience_min": 2,
    },
}


def _cv(nom, titre, annees, debut, fin, poste, employeur, missions, competences, diplome):
    return (
        f"{nom}\n{titre}\nEmail : {nom.split()[0].lower()}.{nom.split()[1].lower()}@mail.fr\n\n"
        f"{annees} ans d'expérience.\n\nEXPÉRIENCE\n{debut} - {fin} : {poste} chez {employeur}\n"
        f"{missions}\n\nCOMPÉTENCES : {competences}\n\nFORMATION\n{diplome}\n"
    )


# (offre, étiquette pertinent, texte du CV)
CORPUS = [
    # ----- Développeur Web : pertinents -----
    ("dev_web", True, _cv("Martin Dupont", "Développeur Full-Stack", 5, 2021, 2026,
        "Développeur Python / React", "WebCorp",
        "Conception d'API REST FastAPI, frontend React, requêtes PostgreSQL, revues de code.",
        "Python, React, SQL, Git, Docker, FastAPI", "Master Informatique")),
    ("dev_web", True, _cv("Sara Benali", "Ingénieure logiciel", 4, 2022, 2026,
        "Ingénieure études et développement", "Softlab",
        "Applications web Django puis React, modélisation UML, bases MySQL, GitLab CI.",
        "Python, Django, React, SQL, Git, CI/CD, UML", "Diplôme d'ingénieur")),
    ("dev_web", True, _cv("Hugo Lefèvre", "Développeur web", 3, 2023, 2026,
        "Développeur full-stack", "Agence Nova",
        "Sites et applications React / Node, API REST, PostgreSQL, intégration continue.",
        "JavaScript, React, Node.js, SQL, Git, Python", "Licence pro développement web")),
    ("dev_web", True, _cv("Lina Costa", "Développeuse backend", 6, 2019, 2026,
        "Développeuse Python senior", "DataSoft",
        "Microservices Python, API REST, optimisation SQL, encadrement de juniors, React occasionnel.",
        "Python, Flask, SQL, Git, Docker, React", "Master génie logiciel")),
    ("dev_web", True, _cv("Yanis Robert", "Développeur d'applications", 2, 2024, 2026,
        "Développeur junior", "StartIt",
        "Développement de modules React et d'API Python, tests unitaires, Git quotidien.",
        "Python, React, SQL, Git", "BUT Informatique")),
    # ----- Développeur Web : non pertinents -----
    ("dev_web", False, _cv("Claire Morel", "Chargée de communication", 4, 2021, 2025,
        "Chargée de communication", "Agence Pixel",
        "Communiqués de presse, réseaux sociaux, organisation d'événements.",
        "Rédaction, InDesign, réseaux sociaux", "Licence Information-Communication")),
    ("dev_web", False, _cv("Paul Girard", "Commercial secteur IT", 7, 2018, 2025,
        "Ingénieur commercial", "TechSales",
        "Vente de solutions logicielles web et cloud, démonstrations produit, suivi client.",
        "Négociation, CRM, prospection", "Master commerce")),
    ("dev_web", False, _cv("Awa Diop", "Comptable", 5, 2020, 2025,
        "Comptable générale", "FiduPlus",
        "Saisie comptable, déclarations fiscales, rapprochements bancaires, Excel avancé.",
        "Comptabilité, Excel, Sage", "BTS Comptabilité gestion")),
    ("dev_web", False, _cv("Tom Maréchal", "Technicien support", 3, 2022, 2025,
        "Technicien helpdesk", "InfoServices",
        "Assistance utilisateurs niveau 1, tickets, installation de postes Windows.",
        "Windows, support, bureautique", "Bac pro SN")),
    ("dev_web", False, _cv("Julie Perrin", "Graphiste", 6, 2019, 2025,
        "Graphiste print et web", "Studio Forme",
        "Identités visuelles, maquettes de sites, déclinaisons print. Notions de HTML.",
        "Photoshop, Illustrator, HTML", "Bachelor design graphique")),

    # ----- Data Analyst : pertinents -----
    ("data_analyst", True, _cv("Nadia Karim", "Data analyst", 3, 2023, 2026,
        "Data analyst", "RetailMetrics",
        "Préparation de données pandas, requêtes SQL complexes, tableaux de bord Power BI.",
        "Python, pandas, SQL, Power BI, Excel", "Master statistique")),
    ("data_analyst", True, _cv("Lucas Marin", "Analyste de données", 2, 2024, 2026,
        "Analyste BI", "BanqueDirect",
        "Automatisation de reportings Python, nettoyage de données, SQL quotidien, Excel avancé.",
        "Python, SQL, pandas, Excel, numpy", "Master économétrie")),
    ("data_analyst", True, _cv("Emma Roux", "Data analyst junior", 1, 2025, 2026,
        "Data analyst junior", "SantéData",
        "Études statistiques, jointures SQL, scripts pandas, restitutions Excel aux équipes.",
        "Python, pandas, SQL, Excel, scikit-learn", "Licence MIASHS")),
    ("data_analyst", True, _cv("Mehdi Aouad", "Consultant data", 5, 2021, 2026,
        "Consultant data", "ConseilPlus",
        "Missions d'analyse : collecte, nettoyage pandas, modèles scikit-learn, dashboards.",
        "Python, pandas, scikit-learn, SQL, Excel, machine learning", "Diplôme d'ingénieur")),
    ("data_analyst", True, _cv("Chloé Bernard", "Chargée d'études statistiques", 4, 2022, 2026,
        "Chargée d'études", "InstitutSondage",
        "Traitement d'enquêtes en Python, bases SQL, automatisation Excel, data visualisation.",
        "Python, SQL, Excel, pandas", "Master mathématiques appliquées")),
    # ----- Data Analyst : non pertinents -----
    ("data_analyst", False, _cv("Romain Petit", "Développeur mobile", 4, 2021, 2025,
        "Développeur Android", "AppFactory",
        "Applications Android en Kotlin, publication Play Store, intégration d'API.",
        "Kotlin, Java, Git, Android", "Master informatique")),
    ("data_analyst", False, _cv("Inès Fontaine", "Assistante RH", 3, 2022, 2025,
        "Assistante ressources humaines", "GroupeHorizon",
        "Gestion administrative du personnel, plannings, suivi des recrutements, Excel.",
        "Administration, Excel, paie", "Licence RH")),
    ("data_analyst", False, _cv("Karl Weber", "Chef de cuisine", 12, 2013, 2025,
        "Chef de cuisine", "Le Grand Bistrot",
        "Gestion d'une brigade de 8 personnes, création des cartes, commandes fournisseurs.",
        "Cuisine, gestion d'équipe, HACCP", "CAP Cuisine")),
    ("data_analyst", False, _cv("Manon Leroy", "Community manager", 2, 2023, 2025,
        "Community manager", "AgenceBuzz",
        "Animation de comptes sociaux, statistiques d'audience, campagnes sponsorisées.",
        "Réseaux sociaux, rédaction, Canva", "Bachelor communication digitale")),
    ("data_analyst", False, _cv("Adil Naceri", "Technicien de maintenance", 6, 2019, 2025,
        "Technicien maintenance industrielle", "MécaProd",
        "Maintenance préventive et curative de lignes de production, habilitations électriques.",
        "Électrotechnique, mécanique, GMAO", "BTS Maintenance")),

    # ----- Technicien réseau : pertinents -----
    ("tech_reseau", True, _cv("Bruno Marques", "Administrateur réseaux", 6, 2020, 2026,
        "Administrateur systèmes et réseaux", "HostingPro",
        "Commutateurs et routeurs Cisco, serveurs Linux Debian, Active Directory, VMware.",
        "Cisco, TCP/IP, Linux, Windows Server, VMware", "BTS SIO, CCNA")),
    ("tech_reseau", True, _cv("Salma Idrissi", "Technicienne réseaux", 3, 2023, 2026,
        "Technicienne réseaux", "CollectivitéSud",
        "Brassage et VLAN Cisco, supervision réseau, serveurs Windows Server, scripts bash Linux.",
        "Cisco, réseaux, Linux, Windows Server, bash", "BUT Réseaux et télécoms")),
    ("tech_reseau", True, _cv("Kevin Roussel", "Technicien systèmes", 4, 2022, 2026,
        "Technicien systèmes et réseaux", "CliniquePlus",
        "Administration Active Directory, virtualisation VMware, équipements réseau, sauvegardes.",
        "Windows Server, VMware, TCP/IP, Cisco, Linux", "BTS SIO option SISR")),
    ("tech_reseau", True, _cv("Fatou Ndiaye", "Ingénieure réseaux junior", 2, 2024, 2026,
        "Ingénieure réseaux", "TélécomOuest",
        "Configuration Cisco (routage, VLAN), firewalls, serveurs Linux, documentation réseau.",
        "Cisco, TCP/IP, Linux, virtualisation", "Diplôme d'ingénieur réseaux")),
    ("tech_reseau", True, _cv("Damien Collet", "Administrateur infrastructure", 8, 2018, 2026,
        "Administrateur infrastructure", "IndustriaGroup",
        "Parc de 40 serveurs Linux et Windows Server, cœur de réseau Cisco, supervision, VMware.",
        "Linux, Windows Server, Cisco, TCP/IP, VMware, bash", "Licence pro ASUR")),
    # ----- Technicien réseau : non pertinents -----
    ("tech_reseau", False, _cv("Léa Charpentier", "Développeuse web", 3, 2022, 2025,
        "Développeuse front-end", "WebAgence",
        "Interfaces React et Vue, intégration HTML/CSS, collaboration avec les designers.",
        "JavaScript, React, HTML, CSS, Git", "Licence pro web")),
    ("tech_reseau", False, _cv("Olivier Blanc", "Vendeur en téléphonie", 5, 2020, 2025,
        "Conseiller de vente", "MobileStore",
        "Vente de forfaits et terminaux, conseils réseaux mobiles 4G/5G aux clients.",
        "Vente, relation client, encaissement", "Bac pro commerce")),
    ("tech_reseau", False, _cv("Camille Aubert", "Infirmière", 9, 2016, 2025,
        "Infirmière diplômée d'État", "CHU Centre",
        "Soins en service de médecine, coordination avec l'équipe, transmissions informatisées.",
        "Soins, organisation, dossier patient", "Diplôme d'État infirmier")),
    ("tech_reseau", False, _cv("Nathan Picard", "Data engineer", 4, 2021, 2025,
        "Data engineer", "CloudData",
        "Pipelines de données Python, entrepôts SQL, orchestration, déploiements Docker.",
        "Python, SQL, Docker, git", "Master big data")),
    ("tech_reseau", False, _cv("Sophie Garnier", "Assistante de direction", 11, 2014, 2025,
        "Assistante de direction", "JurisConseil",
        "Agendas, comptes rendus, organisation de déplacements, accueil téléphonique.",
        "Bureautique, organisation, accueil", "BTS Assistant manager")),

    # ----- Cas limites (profils frontière, plus difficiles à classer) -----
    ("dev_web", True, _cv("Antoine Vidal", "Développeur backend", 4, 2022, 2026,
        "Développeur backend Python", "ApiFirst",
        "API REST Python, bases PostgreSQL, Git ; pas de frontend mais forte appétence.",
        "Python, SQL, Git, Flask, Docker", "Master informatique")),
    ("dev_web", False, _cv("Marc Hubert", "Webmaster", 5, 2020, 2025,
        "Webmaster WordPress", "PME Solutions",
        "Maintenance de sites WordPress, intégration HTML/CSS, petites requêtes SQL, Git basique.",
        "WordPress, HTML, CSS, SQL, Git, PHP", "Autodidacte, Bac STMG")),
    ("data_analyst", True, _cv("Laure Mathieu", "Analyste reporting", 3, 2023, 2026,
        "Analyste reporting", "AssurOuest",
        "Reportings SQL et Excel, automatisations pandas récentes, indicateurs métier.",
        "SQL, Excel, pandas, Power BI", "Licence économie-gestion")),
    ("data_analyst", False, _cv("Damir Kovac", "Contrôleur de gestion", 7, 2018, 2025,
        "Contrôleur de gestion", "IndusGroupe",
        "Budgets et clôtures, tableaux de bord Excel, extractions SQL ponctuelles.",
        "Excel, SQL, comptabilité analytique", "Master CCA")),
    ("tech_reseau", True, _cv("Élodie Faure", "Administratrice systèmes", 3, 2023, 2026,
        "Administratrice systèmes", "EduRégion",
        "Serveurs Linux et Windows Server, VLAN et brassage, supervision ; Cisco en cours de certification.",
        "Linux, Windows Server, TCP/IP, bash", "BUT Réseaux")),
    ("tech_reseau", False, _cv("Quentin Morel", "Ingénieur DevOps", 4, 2021, 2025,
        "Ingénieur DevOps", "CloudNative",
        "Déploiements Kubernetes sur Linux, pipelines CI/CD, scripts bash, conteneurs Docker.",
        "Linux, Docker, Kubernetes, bash, CI/CD, git", "Master cloud computing")),
    ("dev_web", False, _cv("Théo Lambert", "Étudiant en informatique", 1, 2025, 2026,
        "Stagiaire développeur", "WebCorp",
        "Stage de 6 mois : petites fonctionnalités React, scripts Python, requêtes SQL, Git.",
        "Python, React, SQL, Git", "BUT Informatique en cours")),
    ("data_analyst", True, _cv("Anaïs Berger", "Analyste de données", 4, 2022, 2026,
        "Analyste de données", "ÉnergieVerte",
        "Analyses statistiques en R, requêtes SQL avancées, restitutions Excel et Tableau.",
        "R, SQL, Excel, Tableau, statistiques", "Master statistique")),
]
