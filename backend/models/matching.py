from extensions import db
from datetime import datetime

class Matching(db.Model):
    __tablename__ = 'matchings'

    id            = db.Column(db.Integer, primary_key=True)
    mentor_id     = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    mentore_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score         = db.Column(db.Float, nullable=False, default=0.0)
    statut        = db.Column(db.Enum('propose','accepte','refuse','actif','termine'), nullable=False, default='propose')
    date_matching = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
