# =============================================================
# routes/messagerie.py — IFRI_MentorLink · Groupe 45
# Module Messagerie : routes HTTP + événements SocketIO
# Auteur : SOULE Moubarak (base) · complété B05
# =============================================================

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from extensions import db, socketio
from models.conversation import Conversation
from models.message import Message
from models.notification import Notification

messagerie_bp = Blueprint('messagerie', __name__)


# ══════════════════════════════════════════════════════════════
# ROUTES HTTP
# ══════════════════════════════════════════════════════════════

@messagerie_bp.route('/conversations', methods=['GET'])
@login_required
def conversations():
    """
    Liste toutes les conversations de l'utilisateur connecté.
    Un utilisateur voit une conversation s'il est mentor OU mentoré
    dans le matching lié.
    """
    from models.matching import Matching

    conversations = (
        db.session.query(Conversation)
        .join(Matching, Conversation.matching_id == Matching.id)
        .filter(
            (Matching.mentor_id == current_user.id) |
            (Matching.mentore_id == current_user.id)
        )
        .order_by(Conversation.date_creation.desc())
        .all()
    )

    result = []
    for conv in conversations:
        dernier_msg = (
            db.session.query(Message)
            .filter_by(conversation_id=conv.id)
            .order_by(Message.date_envoi.desc())
            .first()
        )
        result.append({
            'id': conv.id,
            'matching_id': conv.matching_id,
            'date_creation': conv.date_creation.isoformat(),
            'dernier_message': dernier_msg.contenu if dernier_msg else None,
            'dernier_message_date': (
                dernier_msg.date_envoi.isoformat() if dernier_msg else None
            ),
        })

    return render_template('messagerie/conversations.html', conversations=conversations)


@messagerie_bp.route('/conversations/<int:conv_id>', methods=['GET'])
@login_required
def historique(conv_id):
    """
    Retourne tous les messages d'une conversation (du plus ancien
    au plus récent). Vérifie que l'utilisateur fait partie du matching.
    Marque automatiquement les messages reçus comme lus.
    """
    from models.matching import Matching

    conv = db.session.get(Conversation, conv_id)
    if not conv:
        return jsonify({'error': 'Conversation introuvable'}), 404

    matching = db.session.get(Matching, conv.matching_id)
    if not matching:
        return jsonify({'error': 'Matching introuvable'}), 404

    if current_user.id not in (matching.mentor_id, matching.mentore_id):
        return jsonify({'error': 'Accès refusé'}), 403

    msgs = (
        db.session.query(Message)
        .filter_by(conversation_id=conv_id)
        .order_by(Message.date_envoi.asc())
        .all()
    )

    # Marquer comme lus les messages reçus (pas envoyés par moi)
    for msg in msgs:
        if not msg.lu and msg.expediteur_id != current_user.id:
            msg.lu = True
    db.session.commit()

    result = [{
        'id': m.id,
        'expediteur_id': m.expediteur_id,
        'contenu': m.contenu,
        'date_envoi': m.date_envoi.isoformat(),
        'lu': m.lu
    } for m in msgs]

    return jsonify(result), 200


@messagerie_bp.route('/conversations', methods=['POST'])
@login_required
def creer_conversation():
    """
    Crée une conversation pour un matching donné.
    Si une conversation existe déjà pour ce matching, la retourne
    sans en créer une nouvelle (UNIQUE sur matching_id).
    """
    from models.matching import Matching

    data = request.get_json()
    if not data or not data.get('matching_id'):
        return jsonify({'error': 'matching_id requis'}), 400

    matching = db.session.get(Matching, data['matching_id'])
    if not matching:
        return jsonify({'error': 'Matching introuvable'}), 404

    if current_user.id not in (matching.mentor_id, matching.mentore_id):
        return jsonify({'error': 'Accès refusé'}), 403

    # UNIQUE sur matching_id — vérifier avant INSERT
    existante = (
        db.session.query(Conversation)
        .filter_by(matching_id=data['matching_id'])
        .first()
    )
    if existante:
        return jsonify({
            'id': existante.id,
            'message': 'Conversation déjà existante'
        }), 200

    conv = Conversation(matching_id=data['matching_id'])
    db.session.add(conv)
    db.session.commit()

    return jsonify({'id': conv.id, 'matching_id': conv.matching_id}), 201


# ══════════════════════════════════════════════════════════════
# ÉVÉNEMENTS SOCKETIO — Messagerie temps réel
# ══════════════════════════════════════════════════════════════

@socketio.on('join_conversation')
def on_join(data):
    """
    Le client rejoint la room SocketIO de la conversation.
    À appeler dès que l'utilisateur ouvre une conversation.
    data = {'conversation_id': <int>}
    """
    room = str(data['conversation_id'])
    join_room(room)
    emit('status', {'msg': f'Connecté à la conversation {room}'}, room=room)


@socketio.on('send_message')
def handle_send_message(data):
    """
    Reçoit un message, le sauvegarde en BDD, l'émet en temps réel
    à tous les membres de la room (mentor + mentoré).
    data = {'conversation_id': <int>, 'contenu': <str>}
    L'expediteur_id vient de current_user — jamais du client.
    """
    conv_id = data.get('conversation_id')
    contenu = data.get('contenu', '').strip()

    if not conv_id or not contenu:
        emit('error', {'msg': 'Données manquantes'})
        return

    conv = db.session.get(Conversation, conv_id)
    if not conv:
        emit('error', {'msg': 'Conversation introuvable'})
        return

    # Sauvegarde en BDD
    msg = Message(
        conversation_id=conv_id,
        expediteur_id=current_user.id,
        contenu=contenu
    )
    db.session.add(msg)
    db.session.commit()

    # Émission temps réel à toute la room
    emit('new_message', {
        'id': msg.id,
        'conversation_id': msg.conversation_id,
        'expediteur_id': msg.expediteur_id,
        'contenu': msg.contenu,
        'date_envoi': msg.date_envoi.isoformat(),
        'lu': msg.lu
    }, room=str(conv_id))
