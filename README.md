# IFRI_MentorLink — PIL1_2526_45

DEMO via ce lien → https://youtu.be/CBlXgYO_cqM?si=v1yHHa0KiifTFX5-

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

---

### 🐧 Ubuntu / Linux

```bash
# 1. Installer les outils nécessaires
sudo apt update
sudo apt install git python3 python3-pip python3-venv mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql

# 2. Cloner le dépôt
git clone https://github.com/hounyojoachim-debug/PIL1_2526_45.git
cd PIL1_2526_45

# 3. Environnement virtuel
cd backend
python3 -m venv venv
source venv/bin/activate

# 4. Installer les dépendances Python
pip install -r ../requirements.txt
pip install cryptography

# 5. Configurer MySQL (première fois uniquement)
# Si MySQL vient d'être installé, connectez-vous avec sudo :
sudo mysql
# Dans MySQL, tapez :
# ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'root1234';
# FLUSH PRIVILEGES;
# EXIT;

# 6. Créer la BDD et importer le schéma (une seule commande)
mysql -u root -proot1234 < ../schema.sql

# 7. Charger les données de test
mysql -u root -proot1234 ifri_mentorlink < data_test.sql

# 8. Créer le fichier .env dans backend/
echo 'DATABASE_URL=mysql+pymysql://root:root1234@localhost/ifri_mentorlink' > .env
echo 'SECRET_KEY=mentorlink-secret-group45' >> .env

# 9. Lancer l'application
python3 app.py
```

> ⚠️ Remplacez `root1234` par votre mot de passe MySQL si différent.

---

### 🪟 Windows

> **Important :** Toutes les commandes Windows doivent être exécutées dans **Git Bash**, pas dans PowerShell.

**Étape 1 — Installer Git**
Télécharger sur https://git-scm.com/download/win → installer avec tous les paramètres par défaut.

**Étape 2 — Installer Python**
Télécharger sur https://python.org/downloads → lors de l'installation, **cocher "Add Python to PATH"**.

**Étape 3 — Installer MySQL**
Télécharger MySQL Community Server sur https://dev.mysql.com/downloads/installer/ → choisir "Server only" → lors de la configuration, définir un mot de passe root (notez-le bien).

**Étape 4 — Ouvrir Git Bash** (menu Démarrer → Git Bash)

```bash
# 5. Ajouter MySQL au PATH (à faire à chaque ouverture de Git Bash)
export PATH=$PATH:"/c/Program Files/MySQL/MySQL Server 8.0/bin"

# 6. Cloner le dépôt
git clone https://github.com/hounyojoachim-debug/PIL1_2526_45.git
cd PIL1_2526_45

# 7. Environnement virtuel
cd backend
python -m venv venv

# Autoriser l'exécution de scripts (dans PowerShell, une seule fois) :
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activer le venv dans Git Bash :
source venv/Scripts/activate

# 8. Installer les dépendances Python
pip install -r ../requirements.txt
pip install cryptography

# 9. Créer la BDD et importer le schéma
mysql -u root -pVOTRE_MDP < ../schema.sql

# 10. Charger les données de test
mysql -u root -pVOTRE_MDP ifri_mentorlink < data_test.sql

# 11. Créer le fichier .env dans backend/
echo 'DATABASE_URL=mysql+pymysql://root:VOTRE_MDP@localhost/ifri_mentorlink' > .env
echo 'SECRET_KEY=mentorlink-secret-group45' >> .env

# 12. Lancer l'application
python app.py
```

> ⚠️ Remplacez `VOTRE_MDP` par votre mot de passe MySQL défini lors de l'installation.

---

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

## Démo messagerie temps réel

Pour tester la messagerie SocketIO :
1. Ouvre **Chrome** → connecte-toi avec `tobie@ifri.bj`
2. Ouvre **Firefox** → connecte-toi avec `moubarak@ifri.bj`
3. Ouvre la même conversation dans les deux navigateurs
4. Envoie un message → il apparaît instantanément dans l'autre navigateur

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
