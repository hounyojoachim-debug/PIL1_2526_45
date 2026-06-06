# =============================================================
# models/__init__.py — IFRI_MentorLink · Groupe 45
# Importe tous les models pour que SQLAlchemy les connaisse
# =============================================================

# Branche 03
from models.user          import User
from models.competence    import Competence, UserCompetence
from models.disponibilite import Disponibilite

# Branche 04
from models.offre    import OffreDemande, OffreDemandCompetence
from models.matching import Matching

# Branche 05
from models.conversation import Conversation
from models.message      import Message
from models.notification import Notification
