# 🐾 Tâches du Jour

Bienvenue sur **Tâches du Jour**, une application web pédagogique simple et bienveillante pour organiser ses activités quotidiennes dans une ambiance chaleureuse accompagnée d'illustrations de chiens et de citations positives.

---

## 🎯 Vocation Pédagogique & Principes

Ce projet a été conçu selon des principes de gouvernance stricts (définis dans la constitution du projet) :
1. **Simplicité et clarté** : Code lisible, compréhensible par des apprenants, sans abstraction prématurée ni complexité superflue (KISS, YAGNI).
2. **Stack épurée** :
   - **Frontend** : HTML5 sémantique et CSS3 moderne pur (Custom Properties, Flexbox) — *zéro framework JavaScript*.
   - **Backend** : Python 3.10+ avec **Flask** comme unique dépendance serveur (patron Post/Redirect/Get).
3. **Tests automatisés obligatoires** : 100 % de la logique applicative et des routes est couverte par des tests automatisés avec **pytest**.
4. **Minimalisme des dépendances** : Uniquement `flask` et `pytest` dans `requirements.txt`.
5. **Hygiène de sécurité** : Aucune donnée sensible dans le dépôt, persistance locale dans un fichier JSON propre (`data/tasks.json`).

---

## 🏗️ Structure du Projet

```text
taches-du-jour/
├── app/
│   ├── __init__.py          # Fabrique applicative Flask (create_app)
│   ├── models.py            # Modèle Task et gestionnaire de persistance JSON
│   ├── routes.py            # Routes HTTP (GET /, POST /tasks, POST /tasks/<id>/complete)
│   ├── quotes.py            # Collection de citations positives et canines
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Styles CSS3 chaleureux et adaptatifs
│   │   └── images/
│   │       └── dogs/        # Illustrations vectorielles SVG locales
│   └── templates/
│       ├── base.html        # Gabarit HTML5 sémantique
│       └── index.html       # Page principale (formulaire, liste, citation)
├── data/
│   └── tasks.json           # Persistance locale automatique des tâches
├── tests/
│   ├── conftest.py          # Fixtures pytest hermétiques (tmp_path, test_client)
│   ├── test_models.py       # Tests unitaires du modèle et de la persistance
│   └── test_routes.py       # Tests d'intégration des routes et scénarios HTTP
├── requirements.txt         # Dépendances déclarées (flask, pytest)
├── run.py                   # Script d'exécution du serveur de développement
└── README.md                # Documentation pédagogique du projet
```

---

## 🚀 Installation & Démarrage

### 1. Prérequis
- Python 3.10 ou supérieur installé.

### 2. Cloner et configurer l'environnement virtuel

```bash
# Créer l'environnement virtuel
python3 -m venv .venv

# Activer l'environnement virtuel
# Sur Linux / macOS :
source .venv/bin/activate
# Sur Windows :
# .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Exécuter les tests automatisés

```bash
pytest -v
```

### 4. Lancer l'application

```bash
python run.py
```

Ouvrez votre navigateur sur : **[http://localhost:5000](http://localhost:5000)**.

---

## 💡 Fonctionnalités

- **Ajout en chaîne fluide** : Saisissez l'intitulé d'une tâche et validez (Entrée ou clic). Le formulaire se réinitialise instantanément pour vous permettre d'ajouter la mission suivante.
- **Liste et suivi** : Consultez vos tâches ordonnées et cochez-les au fur et à mesure de votre progression.
- **Barre de progression en temps réel** : Visualisez d'un coup d'œil le décompte des tâches terminées sur le total et suivez votre avancement grâce à une jauge graphique animée et accessible (attributs WAI-ARIA natifs).
- **Célébration festive de fin de journée** : Dès que 100 % de vos tâches sont terminées, une bannière festive exclusive avec un joyeux chiot célébrant votre victoire (`dog-cheer.svg`) s'affiche pour valoriser vos efforts !
- **Persistance locale** : Vos tâches restent enregistrées dans `data/tasks.json` même si vous arrêtez le serveur.
- **Ambiance chaleureuse** : Profitez de citations bienveillantes et d'illustrations canines encourageantes tout au long de votre journée.
