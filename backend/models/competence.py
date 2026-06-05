# =============================================================
# models/competence.py — IFRI_MentorLink · Groupe 45
# Models : tables competences + user_competences
# =============================================================

from extensions import db


class Competence(db.Model):
    """Référentiel des matières disponibles (Algorithmique, Python, Réseaux...)"""

    __tablename__ = 'competences'

    id        = db.Column(db.Integer, primary_key=True)
    nom       = db.Column(db.String(150), nullable=False)
    categorie = db.Column(db.String(100), nullable=False)

    # Liaison vers les associations user_competences
    user_competences = db.relationship(
        'UserCompetence',
        backref='competence',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Competence {self.id} — {self.nom}>'


class UserCompetence(db.Model):
    """
    Table de liaison users ↔ competences.
    Clé primaire composite (user_id + competence_id) — pas de doublon possible.
    type = 'maitrise' (peut enseigner) ou 'a_ameliorer' (veut apprendre)
    """

    __tablename__ = 'user_competences'

    # Clé primaire composite : une seule ligne par paire (user, compétence)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    competence_id = db.Column(
        db.Integer,
        db.ForeignKey('competences.id', ondelete='CASCADE'),
        primary_key=True
    )

    type = db.Column(
        db.Enum('maitrise', 'a_ameliorer'),
        nullable=False
    )

    def __repr__(self):
        return f'<UserCompetence user={self.user_id} competence={self.competence_id} [{self.type}]>'
