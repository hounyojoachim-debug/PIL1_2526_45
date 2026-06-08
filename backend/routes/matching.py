from flask import Blueprint, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.matching import Matching
from models.competence import UserCompetence, Competence
from models.disponibilite import Disponibilite

matching_bp = Blueprint('matching', __name__)

def calculer_score(mentor, mentore, disponibilites):

    # COMPETENCES
    matieres_communes = set(mentor["points_forts"]) & set(mentore["points_faibles"])
    total_besoins = len(mentore["points_faibles"])

    if total_besoins > 0:
        score_competences = (len(matieres_communes) / total_besoins) * 60
    else:
        score_competences = 0

    # DISPONIBILITES
    dispo_mentor  = set(disponibilites.get(mentor["id"], []))
    dispo_mentore = set(disponibilites.get(mentore["id"], []))
    creneaux_communs = dispo_mentor & dispo_mentore
    total_creneaux = len(dispo_mentore)

    if total_creneaux > 0:
        score_dispos = (len(creneaux_communs) / total_creneaux) * 30
    else:
        score_dispos = 0

    # FILIERE
    fillieres_proches = {frozenset({"SI", "GL"}), frozenset({"IA", "IM"})}
    paire = frozenset({mentor["filiere"], mentore["filiere"]})

    if mentor["filiere"] == mentore["filiere"]:
        score_filiere = 10
    elif paire in fillieres_proches:
        score_filiere = 6
    else:
        score_filiere = 0

    return round(min(score_competences + score_dispos + score_filiere, 100.0), 2)


@matching_bp.route('/suggestions', methods=['GET'])
@login_required
def suggestions():
    tous_users = User.query.filter(User.id != current_user.id, User.actif == True).all()

    disponibilites = {}
    for u in tous_users + [current_user]:
        dispos = Disponibilite.query.filter_by(user_id=u.id).all()
        disponibilites[u.id] = [f"{d.jour}_{d.heure_debut}" for d in dispos]

    def profil(u):
        competences = UserCompetence.query.filter_by(user_id=u.id).all()
        return {
            "id": u.id,
            "filiere": u.filiere,
            "points_forts":  [c.competence_id for c in competences if c.type == 'maitrise'],
            "points_faibles": [c.competence_id for c in competences if c.type == 'a_ameliorer']
        }

    # Dictionnaire id → nom pour les compétences
    noms_comp = {c.id: c.nom for c in Competence.query.all()}

    moi = profil(current_user)
    resultats = []

    for u in tous_users:
        p = profil(u)
        score = calculer_score(p, moi, disponibilites)
        if score > 0:
            comp_communes = set(p["points_forts"]) & set(moi["points_faibles"])
            dispo_mentor  = set(disponibilites.get(u.id, []))
            dispo_moi     = set(disponibilites.get(current_user.id, []))
            dispo_communes = dispo_mentor & dispo_moi
            resultats.append({
                'mentor_prenom': u.prenom,
                'mentor_nom': u.nom,
                'mentor_filiere': u.filiere,
                'mentor_niveau': u.niveau,
                'mentor_id': u.id,
                'score': score,
                'competences_communes': [noms_comp.get(c, str(c)) for c in comp_communes],
                'dispos_communes': list(dispo_communes)
            })

    resultats.sort(key=lambda x: x['score'], reverse=True)
    # Mentorés potentiels — ceux que MOI je peux aider
    mentores = []
    for u in tous_users:
        p = profil(u)
        score = calculer_score(moi, p, disponibilites)
        if score > 0:
            comp_communes_m = set(moi["points_forts"]) & set(p["points_faibles"])
            dispo_u   = set(disponibilites.get(u.id, []))
            dispo_moi2 = set(disponibilites.get(current_user.id, []))
            dispo_communes_m = dispo_u & dispo_moi2
            mentores.append({
                'mentor_prenom': u.prenom,
                'mentor_nom':    u.nom,
                'mentor_filiere': u.filiere,
                'mentor_niveau':  u.niveau,
                'mentor_id':      u.id,
                'score':          score,
                'competences_communes': [noms_comp.get(c, str(c)) for c in comp_communes_m],
                'dispos_communes': list(dispo_communes_m)
            })
    mentores.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'suggestions': resultats, 'mentores': mentores})

@matching_bp.route('/contacter/<int:mentor_id>', methods=['POST'])
@login_required
def contacter(mentor_id):
    """
    Crée un matching + une conversation entre current_user (mentoré)
    et mentor_id. Si ça existe déjà, récupère l'existant.
    Redirige vers le chat.
    """
    from models.matching    import Matching
    from models.conversation import Conversation
    from models.disponibilite import Disponibilite

    # Calculer le score pour ce mentor
    def profil(u):
        comps = UserCompetence.query.filter_by(user_id=u.id).all()
        return {
            "id": u.id,
            "filiere": u.filiere,
            "points_forts":   [c.competence_id for c in comps if c.type == "maitrise"],
            "points_faibles": [c.competence_id for c in comps if c.type == "a_ameliorer"]
        }

    mentor  = db.session.get(User, mentor_id)
    if not mentor:
        flash("Mentor introuvable.", "danger")
        return redirect(url_for("auth.tableau_de_bord"))

    dispos = {}
    for u in [mentor, current_user]:
        d = Disponibilite.query.filter_by(user_id=u.id).all()
        dispos[u.id] = [f"{x.jour}_{x.heure_debut}" for x in d]

    score = calculer_score(profil(mentor), profil(current_user), dispos)

    # Matching — chercher un existant ou créer
    from sqlalchemy import or_, and_
    matching = Matching.query.filter(
        or_(
            and_(Matching.mentor_id == mentor_id, Matching.mentore_id == current_user.id),
            and_(Matching.mentor_id == current_user.id, Matching.mentore_id == mentor_id)
        )
    ).first()
    if not matching:
        matching = Matching(
            mentor_id=mentor_id,
            mentore_id=current_user.id,
            score=score,
            statut="actif"
        )
        db.session.add(matching)
        db.session.commit()

    # Conversation — chercher une existante ou créer
    conv = Conversation.query.filter_by(matching_id=matching.id).first()
    if not conv:
        conv = Conversation(matching_id=matching.id)
        db.session.add(conv)
        db.session.commit()

    return redirect(url_for("messagerie.chat", conv_id=conv.id))
