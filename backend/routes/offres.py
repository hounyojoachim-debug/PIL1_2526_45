from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.offre import OffreDemande, OffreDemandCompetence

offres_bp = Blueprint('offres', __name__)

@offres_bp.route('/', methods=['GET'])
@login_required
def liste_offres():
    offres = OffreDemande.query.filter_by(statut='actif').all()
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
    type_val    = request.form.get('type_offre', 'offre')
    offre = OffreDemande(
        user_id=current_user.id,
        type=type_val,
        format_seance=format_val,
        description=description
    )
    db.session.add(offre)
    db.session.commit()
    flash('Offre publiée avec succès !' if type_val == 'offre' else 'Demande publiée avec succès !', 'success')
    return redirect(url_for('offres.liste_offres'))

@offres_bp.route('/<int:offre_id>/modifier', methods=['GET'])
@login_required
def modifier_offre(offre_id):
    offre = db.session.get(OffreDemande, offre_id)
    if not offre or offre.user_id != current_user.id:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('offres.liste_offres'))
    return render_template('offres/modifier.html', offre=offre)

@offres_bp.route('/<int:offre_id>/modifier', methods=['POST'])
@login_required
def sauvegarder_offre(offre_id):
    offre = db.session.get(OffreDemande, offre_id)
    if not offre or offre.user_id != current_user.id:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('offres.liste_offres'))
    offre.type          = request.form.get('type_offre', offre.type)
    offre.description   = request.form.get('description', offre.description)
    offre.format_seance = request.form.get('format', offre.format_seance)
    db.session.commit()
    flash('Offre mise à jour avec succès !', 'success')
    return redirect(url_for('offres.liste_offres'))

@offres_bp.route('/<int:offre_id>/supprimer', methods=['POST'])
@login_required
def supprimer_offre(offre_id):
    offre = db.session.get(OffreDemande, offre_id)
    if not offre or offre.user_id != current_user.id:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('offres.liste_offres'))
    db.session.execute(db.text("DELETE FROM offres_demandes_competences WHERE offre_demande_id = :id"), {"id": offre_id})
    db.session.execute(db.text("DELETE FROM offres_demandes WHERE id = :id"), {"id": offre_id})
    db.session.commit()
    flash('Offre supprimée.', 'success')
    return redirect(url_for('offres.liste_offres'))
