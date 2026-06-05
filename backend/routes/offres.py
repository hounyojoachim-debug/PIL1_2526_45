from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.offre import OffreDemande, OffreDemandCompetence

offres_bp = Blueprint('offres', __name__)

@offres_bp.route('/offres', methods=['GET'])
@login_required
def liste_offres():
    offres = OffreDemande.query.filter_by(type='offre', statut='actif').all()
    return jsonify([{
        'id': o.id,
        'user_id': o.user_id,
        'format': o.format,
        'description': o.description
    } for o in offres])

@offres_bp.route('/offres', methods=['POST'])
@login_required
def creer_offre():
    data = request.get_json()
    offre = OffreDemande(
        user_id=current_user.id,
        type=data.get('type', 'offre'),
        format=data.get('format', 'les_deux'),
        description=data.get('description', '')
    )
    db.session.add(offre)
    db.session.commit()
    return jsonify({'message': 'Offre créée', 'id': offre.id}), 201
