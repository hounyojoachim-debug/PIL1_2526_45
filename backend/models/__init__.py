# =============================================================
# models/__init__.py — IFRI_MentorLink · Groupe 45
# Importe tous les models pour que SQLAlchemy les connaisse
# au démarrage de l'application.
#
# RÈGLE : chaque nouvelle branche qui crée un model
#         DOIT l'ajouter ici.
# =============================================================

# ── Branche 03 — Module Auth & Profils ───────────────────────
from models.user          import User           # noqa
from models.competence    import Competence, UserCompetence  # noqa
from models.disponibilite import Disponibilite  # noqa

# ── Branche 04 — Module Matching (à décommenter en B04) ──────
# from models.offre        import OffreDemande, OffreDemandCompetence  # noqa
# from models.matching     import Matching                              # noqa

# ── Branche 05 — Module Messagerie (à décommenter en B05) ────
# from models.conversation import Conversation  # noqa
# from models.message      import Message       # noqa
# from models.notification import Notification  # noqa
