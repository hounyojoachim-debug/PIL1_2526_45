# =============================================================
# models/user.py — IFRI_MentorLink · Groupe 45
# Model SQLAlchemy : table users
# Sécurité : bcrypt (hash/verify) · Flask-Login (sessions)
# =============================================================

from extensions import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime


# =============================================================
# user_loader — OBLIGATOIRE pour Flask-Login
# =============================================================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =============================================================
# Model User
# =============================================================
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    # ── Colonnes ──────────────────────────────────────────────
    id               = db.Column(db.Integer, primary_key=True)
    nom              = db.Column(db.String(100), nullable=False)
    prenom           = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(255), nullable=False, unique=True)
    telephone        = db.Column(db.String(20),  nullable=False, unique=True)
    mot_de_passe     = db.Column(db.String(255), nullable=False)
    filiere          = db.Column(db.Enum('SI', 'GL', 'IA', 'IM', 'RS', 'Autre'), nullable=False)
    niveau           = db.Column(db.Enum('L1', 'L2', 'L3', 'M1', 'M2'), nullable=False)
    photo            = db.Column(db.String(255), nullable=True, default=None)
    bio              = db.Column(db.Text, nullable=True, default=None)
    date_inscription = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actif            = db.Column(db.Boolean, nullable=False, default=True)

    # ── Relationships Branche 03 ───────────────────────────────
    competences    = db.relationship('UserCompetence', backref='user', lazy=True, cascade='all, delete-orphan')
    disponibilites = db.relationship('Disponibilite',  backref='user', lazy=True, cascade='all, delete-orphan')

    # ── Relationships Branche 04 — décommenter en B04 ──────────
    offres = db.relationship('OffreDemande', backref='auteur', lazy=True, cascade='all, delete-orphan')
    matchings_mentor  = db.relationship('Matching', foreign_keys='Matching.mentor_id',  backref='mentor',  lazy=True)
    matchings_mentore = db.relationship('Matching', foreign_keys='Matching.mentore_id', backref='mentore', lazy=True)

    # ── Relationships Branche 05 — décommenter en B05 ──────────
    # messages_envoyes = db.relationship('Message', foreign_keys='Message.expediteur_id', backref='expediteur', lazy=True)
    # notifications    = db.relationship('Notification', backref='destinataire', lazy=True, cascade='all, delete-orphan')

    # ── Flask-Login — override is_active ──────────────────────
    @property
    def is_active(self):
        return self.actif

    # ── Méthodes bcrypt ────────────────────────────────────────
    def set_password(self, mot_de_passe_clair):
        self.mot_de_passe = bcrypt.generate_password_hash(mot_de_passe_clair).decode('utf-8')

    def check_password(self, mot_de_passe_clair):
        return bcrypt.check_password_hash(self.mot_de_passe, mot_de_passe_clair)

    def __repr__(self):
        return f'<User {self.id} — {self.prenom} {self.nom}>'
