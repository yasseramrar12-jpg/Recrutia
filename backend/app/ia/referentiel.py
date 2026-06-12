"""Référentiel de compétences et synonymes.

Le référentiel associe une compétence canonique à la liste des formes
sous lesquelles elle peut apparaître dans un CV. Il est volontairement
extensible : il suffit d'ajouter une entrée au dictionnaire.
"""

REFERENTIEL_COMPETENCES: dict[str, list[str]] = {
    # Langages
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp"],
    "php": ["php"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "mariadb", "sqlite", "pl/sql"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "sass", "scss"],
    "bash": ["bash", "shell"],
    # Frameworks / bibliothèques
    "react": ["react", "reactjs", "react.js"],
    "vue": ["vue", "vuejs", "vue.js"],
    "angular": ["angular", "angularjs"],
    "node.js": ["node", "nodejs", "node.js", "express"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "spring": ["spring", "spring boot", "springboot"],
    "qt": ["qt", "qt5", "qt6"],
    # Data / IA
    "machine learning": ["machine learning", "apprentissage automatique", "ml"],
    "deep learning": ["deep learning", "apprentissage profond"],
    "nlp": ["nlp", "traitement du langage", "traitement automatique du langage"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch", "torch"],
    "power bi": ["power bi", "powerbi"],
    "excel": ["excel"],
    # Outils / DevOps
    "git": ["git", "github", "gitlab"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux", "ubuntu", "debian"],
    "ci/cd": ["ci/cd", "cicd", "jenkins", "github actions", "intégration continue"],
    "rest": ["rest", "api rest", "restful"],
    # Réseaux / systèmes
    "tcp/ip": ["tcp/ip", "tcp", "réseaux"],
    "cisco": ["cisco", "ccna"],
    "windows server": ["windows server", "active directory"],
    "vmware": ["vmware", "virtualisation"],
    # Gestion / méthode
    "agile": ["agile", "scrum", "kanban"],
    "uml": ["uml", "merise"],
    "gestion de projet": ["gestion de projet", "chef de projet"],
}

MOTS_DIPLOMES = [
    "bts", "dut", "but", "licence", "licence pro", "bachelor",
    "master", "ingénieur", "doctorat", "bac+2", "bac+3", "bac+5",
]
