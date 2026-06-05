# =============================================================
# models/message.py — IFRI_MentorLink · Groupe 45
# Model SQLAlchemy : table messages
# Chaque message appartient à une conversation.
# expediteur_id = qui a envoyé le message.
# =============================================================

from extensions import db
from datetime import datetime


class Message(db.Model):

    __tablename__ = 'messages'

    # ── Colonnes ──────────────────────────────────────────────
    id              = db.Column(db.Integer, primary_key=True)

    # FK vers conversations — dans quelle conversation ce message a été envoyé
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey('conversations.id', ondelete='CASCADE'),
        nullable=False
    )

    # FK vers users — qui a envoyé ce message
    # foreign_keys explicite : obligatoire car User aura 2 FK vers messages
    expediteur_id   = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    # Contenu textuel du message
    contenu         = db.Column(db.Text, nullable=False)

    # Date d'envoi automatique
    date_envoi      = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # FALSE = pas encore lu · TRUE = lu par le destinataire
    lu              = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Message {self.id} — conv {self.conversation_id} — exp {self.expediteur_id}>'
