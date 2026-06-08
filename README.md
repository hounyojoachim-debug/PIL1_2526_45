# IFRI_MentorLink — PIL1_2526_45

Plateforme web de mise en relation mentorale entre étudiants IFRI.  
Projet intégrateur 2025-2026 · Groupe 45 · Université d'Abomey-Calavi

---

## Le projet en 30 secondes

IFRI_MentorLink permet aux étudiants de l'IFRI de trouver un mentor ou de proposer leur aide à leurs camarades. Un algorithme calcule automatiquement les meilleures correspondances selon les compétences, les disponibilités et les filières. Une messagerie en temps réel (SocketIO) est intégrée pour organiser les sessions de travail.

**3 modules :** Gestion des comptes et profils · Algorithme de matching · Messagerie instantanée

---

## Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python 3 + Flask (Application Factory) |
| Base de données | MySQL 8 via Flask-SQLAlchemy |
| Frontend | Bootstrap 5 + Jinja2 |
| Messagerie temps réel | Flask-SocketIO |
| Authentification | Flask-Login + bcrypt |
| ORM | SQLAlchemy + PyMySQL |

---

## Lancer l'application en local

### Prérequis
- Python 3.10+
- MySQL 8+
- Git

### Ubuntu / Linux

```bash
# 1. Cloner le dépôt
git clone https://github.com/hounyojoachim-debug/PIL1_2526_45.git
cd PIL1_2526_45/backend

# 2. Environnement virtuel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Créer la BDD
sudo mysql -u root -e "CREATE DATABASE ifri_mentorlink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 4. Importer le schéma
mysql -u root ifri_mentorlink < ../schema.sql

# 5. (Optionnel) Données de test
mysql -u root ifri_mentorlink < data_test.sql

# 6. Fichier .env (à créer dans backend/)
echo 'DATABASE_URL=mysql+pymysql://root:@localhost/ifri_mentorlink' > .env
echo 'SECRET_KEY=mentorlink-secret-group45' >> .env

# 7. Lancer
python3 app.py
```

### Windows

```powershell
# 1. Cloner le dépôt
git clone https://github.com/hounyojoachim-debug/PIL1_2526_45.git
cd PIL1_2526_45\backend

# 2. Environnement virtuel
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3-4. Créer la BDD et importer le schéma via MySQL Workbench ou :
mysql -u root -p -e "CREATE DATABASE ifri_mentorlink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -pVOTRE_MDP ifri_mentorlink < ..\schema.sql

# 5. Fichier .env — créer manuellement dans backend/ avec ce contenu :
# DATABASE_URL=mysql+pymysql://root:VOTRE_MDP@localhost/ifri_mentorlink
# SECRET_KEY=mentorlink-secret-group45

# 6. Lancer
python app.py
```

### Accéder à l'application

Ouvrir dans le navigateur : **http://127.0.0.1:5000/auth/connexion**

---

## Comptes de test

Après avoir chargé `data_test.sql`, ces comptes sont disponibles :

| Email | Mot de passe | Filière |
|---|---|---|
| tobie@ifri.bj | Test1234! | SI |
| moubarak@ifri.bj | Test1234! | SI |
| curtis@ifri.bj | Test1234! | IA |
| charnel@ifri.bj | Test1234! | IM |
| fanelle@ifri.bj | Test1234! | GL |

---

## Structure du projet

```
PIL1_2526_45/
├── backend/
│   ├── app.py              ← Point d'entrée Flask
│   ├── config.py           ← Configuration BDD et clé secrète
│   ├── extensions.py       ← Extensions Flask (db, login, socketio, bcrypt)
│   ├── requirements.txt    ← Dépendances Python
│   ├── data_test.sql       ← Données de test
│   ├── models/             ← Modèles SQLAlchemy (10 tables)
│   ├── routes/             ← Blueprints Flask (auth, profil, offres, matching, messagerie)
│   ├── templates/          ← Templates Jinja2 avec Bootstrap 5
│   └── static/             ← CSS et JS
├── schema.sql              ← Schéma BDD complet
├── index.html              ← Rapport de projet (livrable CDC)
└── README.md               ← Ce fichier
```

---

## L'équipe — Groupe 45

| Nom | Filière | Module |
|---|---|---|
| AMADOU Geduld Tobie Vincent | SI | Chef de projet · Architecture · Auth · Intégration |
| DAKOU MANDO Charnel | IM | Frontend Bootstrap 5 · Templates Jinja2 |
| SOULE Moubarak Issotina | SI | Messagerie · Flask-SocketIO |
| CAKPO Curtis Ulysse | IA | Algorithme de matching (60/30/10) |
| HOUNYO ASSOU Joachim | GL | Module profils |
| ASSOGBAHOU Fanelle Auriane | GL | Base de données · schema.sql |
| ADANMITONDE Fritzell Junior | SI | Documentation · Rapport HTML |

---

## Encadrement

- **Supervision :** M. Ratheil HOUNDJI (ratheilesse)
- **Encadrant :** M. Armand ACCROMBESSI (primearwyn)
- **Encadrante :** Mme Maryse GAHOU (MaryseGAHOU)

---

*IFRI · Université d'Abomey-Calavi · 2025-2026*
