from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.user import User

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
    return render_template('profil/modifier.html', user=current_user)


@profil_bp.route('/modifier', methods=['POST'])
@login_required
def sauvegarder_profil():
    current_user.nom    = request.form.get('nom',    current_user.nom).strip()
    current_user.prenom = request.form.get('prenom', current_user.prenom).strip()
    current_user.bio    = request.form.get('bio',    '').strip()
    db.session.commit()
    flash('Profil mis à jour avec succès !', 'success')
    return redirect(url_for('profil.voir_profil', user_id=current_user.id))
