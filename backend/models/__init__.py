# =============================================================
# models/__init__.py — IFRI_MentorLink · Groupe 45
# Sur feature/messagerie : uniquement les models B05.
# Les imports B03/B04 seront ajoutés par Tobie au merge dans main.
# =============================================================

# ── Branche 05 — Module Messagerie ───────────────────────────
from models.conversation import Conversation  # noqa
from models.message      import Message       # noqa
from models.notification import Notification  # noqa
