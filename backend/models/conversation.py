# =============================================================
# models/conversation.py — IFRI_MentorLink · Groupe 45
# Model SQLAlchemy : table conversations
# Une conversation est liée à exactement 1 matching.
# =============================================================

from extensions import db
from datetime import datetime


class Conversation(db.Model):

    __tablename__ = 'conversations'

    # ── Colonnes ──────────────────────────────────────────────
    id          = db.Column(db.Integer, primary_key=True)

    # FK vers matchings — UNIQUE = 1 conversation par matching max
    matching_id = db.Column(
        db.Integer,
        db.ForeignKey('matchings.id', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )

    date_creation = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # ── Relationships ─────────────────────────────────────────
    # Depuis une conversation, accéder à ses messages
    # cascade='all, delete-orphan' : si on supprime la conversation,
    # tous ses messages sont supprimés aussi automatiquement
    messages = db.relationship(
        'Message',
        backref='conversation',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Conversation {self.id} — matching {self.matching_id}>'
