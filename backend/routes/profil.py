from flask import Blueprint, Flask, render_template, abort,request,flash,redirect,url_for
from models import User
from extensions import db

profil_bp = Blueprint('profil', __name__)
# Route définie pour la fonction, une route=une fonction

@profil_bp.route('/profil/<username>', methods=['GET', 'POST'])
def voir_profil_modifier(username):#username est une parcelle html
# On vérifie si l'user exit, si non on revoie l'erreur abort(404) qui est une erreur classique renvoyé sur les pages web en cas d'erreur

        user = User.query.filter_by(username=username).first_or_404() # Requete SQL sous forme python avec SQLAlchemy, user contient la requete de toute les infos syr l'user
# Si l'user fait une requete 'POST'(Modifier son profil)   

        if request.method == 'POST': # 
# Récupération des données du formulaire html avec user qui est une variable html
                user.username = request.form.get('username')
                user.email = request.form.get('email')
                user.telephone = request.form.get('telephone')
                user.mot_de_passe_securise = request.form.get('mot_de_passe_securise')
                user.filiere = request.form.get('filiere')
                user.niveau = request.form.get('niveau')
                user.photo = request.form.get('photo')
                user.bio = request.form.get('bio')

#Sauvegarde des Modifications
                db.session.commit()
                flash("Profil mis à jour avec succès!!!")     

#Redirection vers la page de mise à jour(redirect est tjrs avec url_for)
                return redirect(url_for('profil.voir_profil', username=user.username))

#Template pour montrer au user son profil
        return render_template('Profil.html',user =user)

    
    
    