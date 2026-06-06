# =============================================================
# models/notification.py — IFRI_MentorLink · Groupe 45
# Model SQLAlchemy : table notifications
# Alerte envoyée à un utilisateur.
# type : message · matching · systeme
# =============================================================

from extensions import db
from datetime import datetime


class Notification(db.Model):

    __tablename__ = 'notifications'

    # ── Colonnes ──────────────────────────────────────────────
    id      = db.Column(db.Integer, primary_key=True)

    # FK vers users — qui reçoit la notification
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    # Texte de la notification
    contenu = db.Column(db.String(500), nullable=False)

    # Type pour filtrer côté frontend
    type    = db.Column(
        db.Enum('message', 'matching', 'systeme'),
        nullable=False
    )

    # FALSE = non lue (badge rouge) · TRUE = lue
    lu      = db.Column(db.Boolean, nullable=False, default=False)

    date_creation = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f'<Notification {self.id} — user {self.user_id} — {self.type}>'
