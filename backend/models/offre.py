from extensions import db
from datetime import datetime

class OffreDemande(db.Model):
    __tablename__ = 'offres_demandes'

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    auteur        = db.relationship('User', foreign_keys='OffreDemande.user_id')
    type          = db.Column(db.Enum('offre', 'demande'), nullable=False)
    format_seance = db.Column(db.Enum('presentiel', 'en_ligne', 'les_deux'), nullable=False)
    description   = db.Column(db.Text, nullable=True)
    statut        = db.Column(db.Enum('actif', 'inactif', 'termine'), nullable=False, default='actif')
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    competences = db.relationship('OffreDemandCompetence', backref='offre_demande', lazy=True, cascade='all, delete-orphan')


class OffreDemandCompetence(db.Model):
    __tablename__ = 'offres_demandes_competences'

    id               = db.Column(db.Integer, primary_key=True)
    offre_demande_id = db.Column(db.Integer, db.ForeignKey('offres_demandes.id', ondelete='CASCADE'), nullable=False)
    competence_id    = db.Column(db.Integer, db.ForeignKey('competences.id',     ondelete='CASCADE'), nullable=False)
