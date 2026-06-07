from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.competence import Competence, UserCompetence
from models.disponibilite import Disponibilite

profil_bp = Blueprint('profil', __name__)


@profil_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def voir_profil(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        flash('Profil introuvable.', 'danger')
        return redirect(url_for('auth.tableau_de_bord'))
    return render_template('profil/voir.html', user=user)


@profil_bp.route('/modifier', methods=['GET'])
@login_required
def modifier_profil():
    competences     = Competence.query.all()
    user_maitrise   = [uc.competence_id for uc in UserCompetence.query.filter_by(user_id=current_user.id, type='maitrise').all()]
    user_ameliorer  = [uc.competence_id for uc in UserCompetence.query.filter_by(user_id=current_user.id, type='a_ameliorer').all()]
    disponibilites  = Disponibilite.query.filter_by(user_id=current_user.id).all()
    return render_template('profil/modifier.html',
        user=current_user,
        competences=competences,
        user_maitrise=user_maitrise,
        user_ameliorer=user_ameliorer,
        disponibilites=disponibilites
    )


@profil_bp.route('/modifier', methods=['POST'])
@login_required
def sauvegarder_profil():
    current_user.nom    = request.form.get('nom',    current_user.nom).strip()
    current_user.prenom = request.form.get('prenom', current_user.prenom).strip()
    current_user.bio    = request.form.get('bio',    '').strip()

    # Supprimer et recréer les compétences
    UserCompetence.query.filter_by(user_id=current_user.id).delete()
    for cid in request.form.getlist('competences_maitrise'):
        db.session.add(UserCompetence(user_id=current_user.id, competence_id=int(cid), type='maitrise'))
    for cid in request.form.getlist('competences_ameliorer'):
        db.session.add(UserCompetence(user_id=current_user.id, competence_id=int(cid), type='a_ameliorer'))

    # Supprimer et recréer les disponibilités
    Disponibilite.query.filter_by(user_id=current_user.id).delete()
    jours  = request.form.getlist('dispo_jour')
    debuts = request.form.getlist('dispo_debut')
    fins   = request.form.getlist('dispo_fin')
    for jour, debut, fin in zip(jours, debuts, fins):
        if jour and debut and fin:
            db.session.add(Disponibilite(user_id=current_user.id, jour=jour, heure_debut=debut, heure_fin=fin))

    db.session.commit()
    flash('Profil mis à jour avec succès !', 'success')
    return redirect(url_for('profil.voir_profil', user_id=current_user.id))
