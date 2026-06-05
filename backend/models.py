# backend/models.py
from extensions import db  # On récupère l'outil de connexion

class User(db.Model):
    __tablename__ = 'users'  # <--- C'est ICI que tu fais le lien avec le nom exact de la table dans ton fichier schema.sql !
    
    # Les colonnes doivent correspondre à ton fichier SQL
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenoms = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False) 