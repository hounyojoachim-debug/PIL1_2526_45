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
    uid    = current_user.id
    nom    = request.form.get('nom',    '').strip()
    prenom = request.form.get('prenom', '').strip()
    bio    = request.form.get('bio',    '').strip()

    competences_maitrise  = request.form.getlist('competences_maitrise')
    # Exclure de ameliorer toute compétence déjà dans maitrise
    competences_ameliorer = [c for c in request.form.getlist('competences_ameliorer') if c not in competences_maitrise]
    jours  = request.form.getlist('dispo_jour')
    debuts = request.form.getlist('dispo_debut')
    fins   = request.form.getlist('dispo_fin')

    # Transaction engine brute — aucune session SQLAlchemy impliquée
    with db.engine.connect() as conn:
        with conn.begin():
            conn.execute(db.text(
                "UPDATE users SET nom=:nom, prenom=:prenom, bio=:bio WHERE id=:id"
            ), {"nom": nom, "prenom": prenom, "bio": bio, "id": uid})

            conn.execute(db.text(
                "DELETE FROM user_competences WHERE user_id = :id"
            ), {"id": uid})
            conn.execute(db.text(
                "DELETE FROM disponibilites WHERE user_id = :id"
            ), {"id": uid})

            for cid in competences_maitrise:
                conn.execute(db.text(
                    "INSERT INTO user_competences (user_id, competence_id, type) VALUES (:u,:c,:t)"
                ), {"u": uid, "c": int(cid), "t": "maitrise"})

            for cid in competences_ameliorer:
                conn.execute(db.text(
                    "INSERT INTO user_competences (user_id, competence_id, type) VALUES (:u,:c,:t)"
                ), {"u": uid, "c": int(cid), "t": "a_ameliorer"})

            for jour, debut, fin in zip(jours, debuts, fins):
                if jour and debut and fin:
                    conn.execute(db.text(
                        "INSERT INTO disponibilites (user_id, jour, heure_debut, heure_fin) VALUES (:u,:j,:d,:f)"
                    ), {"u": uid, "j": jour, "d": debut, "f": fin})

    flash("Profil mis à jour avec succès !", "success")
    return redirect(url_for("profil.voir_profil", user_id=uid))
