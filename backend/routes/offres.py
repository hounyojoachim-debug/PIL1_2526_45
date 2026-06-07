from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.offre import OffreDemande, OffreDemandCompetence

offres_bp = Blueprint('offres', __name__)

@offres_bp.route('/', methods=['GET'])
@login_required
def liste_offres():
    offres = OffreDemande.query.filter_by(type='offre', statut='actif').all()
    return render_template('offres/liste.html', offres=offres)

@offres_bp.route('/creer', methods=['GET'])
@login_required
def creer():
    return render_template('offres/creer.html')

@offres_bp.route('/creer', methods=['POST'])
@login_required
def creer_offre():
    format_val  = request.form.get('format_seance', 'les_deux')
    description = request.form.get('description', '')
    type_val    = request.form.get('type', 'offre')
    offre = OffreDemande(
        user_id=current_user.id,
        type=type_val,
        format_seance=format_val,
        description=description
    )
    db.session.add(offre)
    db.session.commit()
    flash('Offre publiée avec succès !', 'success')
    return redirect(url_for('offres.liste_offres'))
