# 🏥 Flu Vaccination Data API

API FastAPI pour l'analyse des données de vaccination contre la grippe en France - Hackathon EPITECH 2025

## 📋 Description

Cette API exploite les données publiques ouvertes pour développer des solutions innovantes permettant de :
- Prédire les besoins en vaccins
- Optimiser la distribution des vaccins en pharmacie
- Anticiper les passages aux urgences liés à la grippe
- Améliorer l'accès aux soins en identifiant les zones sous-vaccinées
- Analyser la saisonnalité et la corrélation température/grippe

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation locale

1. **Cloner le repository**
```bash
git clone <your-repo-url>
cd LUHACKAX
```

2. **Créer un environnement virtuel**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Préparer les données**
Placez vos fichiers CSV dans `backend/data/raw/` :
- `evolution_actes_region.csv`
- `evolution_doses_region.csv`
- `donnees_meteo.csv`
- `actes_doses_region.csv`

5. **Lancer le serveur**
```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur `http://127.0.0.1:8000`

## 📊 Endpoints disponibles

### 🗺️ Géographie

#### Évolution des actes de vaccination par région
```
GET /api/geographie/evolution-actes-region
```
**Paramètres** :
- `region` (optionnel) : Filtrer par région
- `code` (optionnel) : Code région

**Graphique** : Barres empilées

---

#### Évolution des doses distribuées par région
```
GET /api/geographie/evolution-doses-region
```
**Paramètres** :
- `region` (optionnel) : Filtrer par région
- `code` (optionnel) : Code région

**Graphique** : Barres empilées

---

### 🌡️ Saisonnalité

#### Données météo et grippe
```
GET /api/saisonnalite/donnees-meteo
```
**Paramètres** :
- `nom_usuel` (optionnel) : Station météo
- `annee` (optionnel) : Année
- `mois` (optionnel) : Mois (1-12)

**Graphique** : Courbes multiples (température + taux grippe + incidence)

---

### 📦 Logistique

#### Actes vs Doses par région
```
GET /api/logistique/actes-doses-region
```
**Paramètres** :
- `region` (optionnel) : Filtrer par région

**Graphique** : Barres groupées

---

#### Nombre de pharmacies sur une période
```
GET /api/logistique/nombre-pharmacies-periode
```
**Paramètres** :
- `date_debut` (optionnel) : Date de début (YYYY-MM-DD)
- `date_fin` (optionnel) : Date de fin (YYYY-MM-DD)
- `variable_pharmacie` (optionnel) : Variable spécifique

**Graphique** : Line chart

---

### 🔧 Admin

#### Liste des tables et colonnes
```
GET /api/admin/tables
```
Retourne la structure de toutes les tables chargées dans la base de données.

---

## 📖 Documentation interactive

Swagger UI disponible sur :
```
http://127.0.0.1:8000/docs
```

ReDoc disponible sur :
```
http://127.0.0.1:8000/redoc
```

## 🗂️ Structure du projet
```
LUHACKAX/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── schemas.py           # Modèles SQLAlchemy
│   │   │   └── response_models.py   # Modèles Pydantic
│   │   ├── routers/
│   │   │   ├── geographie.py        # Endpoints géographie
│   │   │   ├── saisonnalite.py      # Endpoints saisonnalité
│   │   │   ├── logistique.py        # Endpoints logistique
│   │   │   └── admin.py             # Endpoints admin
│   │   ├── services/
│   │   │   └── data_loader.py       # Chargement automatique des CSV
│   │   ├── config.py                # Configuration
│   │   ├── database.py              # Configuration base de données
│   │   └── main.py                  # Point d'entrée FastAPI
│   ├── data/
│   │   └── raw/                     # Fichiers CSV sources
│   ├── requirements.txt
│   └── flu_vaccination.db           # Base SQLite (auto-générée)
└── README.md
```

## 🛠️ Technologies utilisées

- **FastAPI** : Framework web moderne et performant
- **SQLAlchemy** : ORM Python
- **SQLite** : Base de données embarquée
- **Pandas** : Manipulation des données CSV
- **Pydantic** : Validation des données
- **Uvicorn** : Serveur ASGI

## 📊 Format des réponses

Toutes les réponses incluent :
- `question` : Description de la requête
- `graphique` : Type de graphique recommandé
- `data` : Données brutes
- `total` : Nombre d'enregistrements
- `chartjs` : Configuration Chart.js prête à l'emploi

### Exemple de réponse
```json
{
  "question": "Évolution des actes de vaccination par région",
  "graphique": "Barres empilées",
  "data": [
    {
      "region": "11 - ILE-DE-France",
      "actes_2021": 1234567,
      "actes_2022": 1345678,
      "actes_2023": 1456789,
      "actes_2024": 1567890,
      "evolution_pct": 27.0
    }
  ],
  "total": 13,
  "chartjs": {
    "type": "bar",
    "data": { ... },
    "options": { ... }
  }
}
```

## 🚢 Déploiement sur Render

### Option 1 : Avec requirements.txt
```bash
# Build Command
pip install -r backend/requirements.txt

# Start Command
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Option 2 : Installation manuelle (si requirements.txt échoue)
```bash
# Build Command
pip install fastapi && pip install uvicorn[standard] && pip install sqlalchemy && pip install pandas && pip install python-multipart && pip install pydantic && pip install python-dotenv

# Start Command
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Variables d'environnement sur Render
```
ENVIRONMENT=production
```

## 🔍 Dépannage

### La base de données est vide
Vérifiez que les fichiers CSV sont bien dans `backend/data/raw/` et redémarrez le serveur.

### Erreur de colonnes
Le système gère automatiquement :
- Les BOM (`\ufeff`)
- Les séparateurs `;` et `,`
- Les parenthèses dans les noms de colonnes
- Les caractères spéciaux comme `%`

### Les données météo sont incomplètes
Par défaut, toutes les données sont chargées. Vérifiez qu'il n'y a pas de paramètre `limit` dans l'URL.

## 📝 Sources des données

- IQVIA : Distribution de vaccins et actes de vaccination en pharmacie
- Santé Publique France : Couvertures vaccinales, passages aux urgences
- Données météorologiques : Stations météo françaises

## 👥 Auteurs

Projet réalisé dans le cadre du Hackathon EPITECH 2025
- **Thème** : Optimisation de la stratégie vaccinale contre la grippe

## 📄 License

Ce projet est sous licence MIT.

## 🎯 Objectifs du hackathon

✅ Développer des modèles prédictifs pour estimer les besoins en vaccins  
✅ Créer des outils de visualisation pour aider les décideurs  
✅ Proposer des solutions pour améliorer la distribution des vaccins  
✅ Identifier les zones sous-vaccinées et proposer des stratégies ciblées

---

**API développée avec ❤️ pour le Hackathon EPITECH 2025**
