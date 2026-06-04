from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room
from datetime import datetime

messagerie_bp = Blueprint("messagerie", _name_)

messages = []


@messagerie_bp.route("/messages/<int:user_id>")
def get_messages(user_id):
    result = [
        m for m in messages
        if m["expediteur_id"] == user_id
        or m["destinataire_id"] == user_id
    ]

    return jsonify(result)


@messagerie_bp.route("/messages", methods=["POST"])
def send_message():
    data = request.json

    if not data.get("contenu"):
        return jsonify({"error": "Message vide"}), 400

    message = {
        "id": len(messages) + 1,
        "expediteur_id": data["expediteur_id"],
        "destinataire_id": data["destinataire_id"],
        "contenu": data["contenu"],
        "timestamp": datetime.utcnow().isoformat(),
        "lu": False
    }

    messages.append(message)

    return jsonify(message), 201


def init_socketio(socketio):

    @socketio.on("join")
    def join(data):
        join_room(str(data["user_id"]))

    @socketio.on("send_message")
    def handle_message(data):

        message = {
            "id": len(messages) + 1,
            "expediteur_id": data["expediteur_id"],
            "destinataire_id": data["destinataire_id"],
            "contenu": data["contenu"],
            "timestamp": datetime.utcnow().isoformat(),
            "lu": False
        }

        messages.append(message)

        emit(
            "new_message",
            message,
            room=str(data["destinataire_id"])
        )