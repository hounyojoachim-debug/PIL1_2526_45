from flask import Blueprint, Flask, render_template, abort
from extensions import SQLAlchemy
from models import User
profil_bp = Blueprint('profil', __name__)
@profil_bp.route('/profil/<username>', methods=['GET'])
# Fonction qui permet de regarder le profil de l'user
def voir_profil(username):

    user = User.query.filter_by(username=username).first() # Requete SQL sous forme python avec SQLAlchemy
# On vérifie si l'user exit, si oui fait le template vers la page html, si non on revoie l'erreur abort(404) qui est une erreur classique renvoyé sur les pages web en cas d'erreur 
    if user is None:
        abort(404)
    return render_template('profil.html', user=user)

    
    