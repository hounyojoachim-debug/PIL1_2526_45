from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.matching import Matching
from models.competence import UserCompetence
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

    moi = profil(current_user)
    resultats = []

    for u in tous_users:
        p = profil(u)
        score = calculer_score(p, moi, disponibilites)
        if score > 0:
            resultats.append({
                'mentor_prenom': u.prenom,
                'mentor_nom': u.nom,
                'mentor_filiere': u.filiere,
                'mentor_niveau': u.niveau,
                'score': score
            })

    resultats.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'suggestions': resultats})
