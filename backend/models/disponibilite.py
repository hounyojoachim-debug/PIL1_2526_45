# =============================================================
# models/disponibilite.py — IFRI_MentorLink · Groupe 45
# Model : table disponibilites
# =============================================================

from extensions import db


class Disponibilite(db.Model):
    """Créneau horaire de disponibilité d'un étudiant pour le mentorat."""

    __tablename__ = 'disponibilites'

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    jour = db.Column(
        db.Enum('lundi', 'mardi', 'mercredi', 'jeudi',
                'vendredi', 'samedi', 'dimanche'),
        nullable=False
    )

    # db.Time = TIME MySQL — format HH:MM:SS
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin   = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<Disponibilite user={self.user_id} {self.jour} {self.heure_debut}-{self.heure_fin}>'
