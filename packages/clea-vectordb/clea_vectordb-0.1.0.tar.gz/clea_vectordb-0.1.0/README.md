# Cléa-VectorDB Backend

Le backend de **Cléa-VectorDB** est une API REST construite avec **FastAPI** pour gérer une base de données vectorielle. Il permet d'ajouter, de mettre à jour, de supprimer et de rechercher des documents en combinant des recherches vectorielles et des filtres basés sur des métadonnées.

---

## 🛠️ Fonctionnalités principales

- **Gestion des documents** :
  - Ajouter, mettre à jour, supprimer et lister des documents.
- **Recherche hybride** :
  - Recherche vectorielle rapide avec embeddings générés par **CamemBERTv2**.
  - Classement précis des résultats avec un modèle **Cross-Encoder**.
- **Support PostgreSQL** :
  - Utilisation de l'extension **pgvector** pour stocker et rechercher des embeddings vectoriels.

---

## 🚧 Structure du projet

```shell
backend/
├── api/                  # Endpoints API
│   ├── database_endpoint.py
│   └── search_endpoint.py
├── vectordb/             # Logique métier principale
│   ├── database.py       # Gestion de la base de données
│   ├── embeddings.py     # Génération d'embeddings
│   ├── ranking.py        # Classement des résultats
│   └── search.py         # Recherche hybride
├── test/                 # Tests unitaires
│   ├── test_database_endpoint.py
│   └── test_search_endpoint.py
├── static/               # Fichiers statiques (favicon, etc.)
│   └── favicon.ico
├── main.py               # Point d'entrée FastAPI
├── pyproject.toml        # Configuration du projet Python
├── requirements.txt      # Dépendances Python
├── start.sh              # Script de démarrage
└── README.md             # Documentation du backend
```

---

## ⚙️ Prérequis

- **Python 3.11+**
- **PostgreSQL** avec l'extension **pgvector**
- **uv** (gestionnaire de projet Python)

---

## 🚀 Installation

1. **Cloner le projet** :

   ```bash
   git clone https://github.com/WillIsback/Clea-VectorDB.git
   cd Clea-VectorDB/backend
   ```

2. **Créer un environnement virtuel** :

   ```bash
   uv venv
   ```

3. **Installer les dépendances** :

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configurer PostgreSQL** :
   - Assurez-vous que PostgreSQL est installé et en cours d'exécution.
   - Ajoutez l'extension `pgvector` :

     ```sql
     CREATE EXTENSION IF NOT EXISTS vector;
     ```

5. **Configurer les variables d'environnement** :
   Créez un fichier `.env` dans le répertoire `backend` avec les informations suivantes :

   ```env
   DB_USER=postgres
   DB_PASSWORD=yourpassword
   DB_NAME=clea_vectordb
   DB_HOST=localhost
   DB_PORT=5432
   MODEL_NAME=camembert-base
   CROSS_ENCODER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
   ```

---

## 🏃‍♂️ Démarrage

1. **Initialiser la base de données** :

   ```bash
   uv python -c "from vectordb.database import init_db; init_db()"
   ```

2. **Lancer le backend** :

   ```bash
   ./start.sh
   ```

3. **Accéder à l'API** :
   - Documentation Swagger : [http://localhost:8080/docs](http://localhost:8080/docs)
   - Documentation ReDoc : [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## 🧪 Tests

Pour exécuter les tests unitaires :

```bash
uv pytest
```

---

## 📂 Endpoints principaux

### Gestion des documents

- **Ajouter des documents** : `POST /database/add_document`
- **Mettre à jour un document** : `PUT /database/update_document`
- **Supprimer un document** : `DELETE /database/delete_document`
- **Lister les documents** : `GET /database/list_documents`

### Recherche hybride

- **Recherche vectorielle et textuelle** : `POST /search/hybrid_search`

---

## 📜 Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
