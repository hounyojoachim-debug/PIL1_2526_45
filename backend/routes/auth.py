# =============================================================
# routes/auth.py — IFRI_MentorLink · Groupe 45
# Module : Inscription · Connexion · Déconnexion
# Branche 03
# =============================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from models.competence import UserCompetence
from models.disponibilite import Disponibilite

auth_bp = Blueprint('auth', __name__)


# =============================================================
# GET /auth/inscription  → affiche le formulaire
# POST /auth/inscription → crée le compte
# =============================================================
@auth_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    # Déjà connecté → pas besoin de s'inscrire
    if current_user.is_authenticated:
        return redirect(url_for('auth.tableau_de_bord'))

    if request.method == 'POST':
        # ── Récupération des champs du formulaire ─────────────
        nom              = request.form.get('nom',              '').strip()
        prenom           = request.form.get('prenom',           '').strip()
        email            = request.form.get('email',            '').strip().lower()
        telephone        = request.form.get('telephone',        '').strip()
        mdp              = request.form.get('mot_de_passe',     '')
        mdp_confirm      = request.form.get('mot_de_passe_confirm', '')
        filiere          = request.form.get('filiere',          '')
        niveau           = request.form.get('niveau',           '')

        # ── Validations ────────────────────────────────────────
        erreurs = []

        # Champs obligatoires non vides
        if not all([nom, prenom, email, telephone, mdp, filiere, niveau]):
            erreurs.append('Tous les champs obligatoires doivent être remplis.')

        # Confirmation mot de passe
        if mdp != mdp_confirm:
            erreurs.append('Les mots de passe ne correspondent pas.')

        # Longueur minimale mot de passe
        if len(mdp) < 8:
            erreurs.append('Le mot de passe doit contenir au moins 8 caractères.')

        # Unicité email — cherche si un compte existe déjà avec cet email
        if User.query.filter_by(email=email).first():
            erreurs.append('Un compte existe déjà avec cet email.')

        # Unicité téléphone — même principe
        if User.query.filter_by(telephone=telephone).first():
            erreurs.append('Un compte existe déjà avec ce numéro de téléphone.')

        # Si au moins une erreur → afficher et rester sur le formulaire
        if erreurs:
            for msg in erreurs:
                flash(msg, 'danger')
            return render_template('auth/inscription.html')

        # ── Création du compte ─────────────────────────────────
        user = User(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            filiere=filiere,
            niveau=niveau
        )
        # Hash bcrypt via la méthode du model — JAMAIS stocker en clair
        user.set_password(mdp)

        db.session.add(user)
        db.session.commit()

        # Sauvegarder compétences maîtrisées
        for cid in request.form.getlist('competences_maitrise'):
            db.session.add(UserCompetence(user_id=user.id, competence_id=int(cid), type='maitrise'))

        # Sauvegarder lacunes
        for cid in request.form.getlist('competences_ameliorer'):
            db.session.add(UserCompetence(user_id=user.id, competence_id=int(cid), type='a_ameliorer'))

        # Sauvegarder disponibilités
        jours  = request.form.getlist('dispo_jour')
        debuts = request.form.getlist('dispo_debut')
        fins   = request.form.getlist('dispo_fin')
        for jour, debut, fin in zip(jours, debuts, fins):
            if jour and debut and fin:
                db.session.add(Disponibilite(user_id=user.id, jour=jour, heure_debut=debut, heure_fin=fin))

        db.session.commit()
        flash('Compte créé avec succès ! Connecte-toi.', 'success')
        return redirect(url_for('auth.connexion'))

    # Méthode GET → on affiche juste le formulaire
    return render_template('auth/inscription.html')


# =============================================================
# GET/POST /auth/connexion
# =============================================================
@auth_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    # Déjà connecté → rediriger directement
    if current_user.is_authenticated:
        return redirect(url_for('auth.tableau_de_bord'))

    if request.method == 'POST':
        identifiant = request.form.get('identifiant', '').strip()
        mdp         = request.form.get('mot_de_passe', '')

        if not identifiant or not mdp:
            flash('Identifiant et mot de passe requis.', 'danger')
            return render_template('auth/connexion.html')

        # ── Chercher par email OU par téléphone ────────────────
        # Cahier des charges : connexion avec "email ou téléphone + mot de passe"
        user = (
            User.query.filter_by(email=identifiant.lower()).first()
            or User.query.filter_by(telephone=identifiant).first()
        )

        # ── Vérifications ─────────────────────────────────────
        # RÈGLE SÉCURITÉ : message d'erreur volontairement vague
        # Ne pas dire "email incorrect" ou "mot de passe incorrect" séparément
        # → un attaquant ne saurait pas ce qui est faux
        if user is None or not user.check_password(mdp):
            flash('Identifiant ou mot de passe incorrect.', 'danger')
            return render_template('auth/connexion.html')

        # Compte désactivé (soft delete)
        if not user.is_active:
            flash('Ce compte a été désactivé. Contacte un administrateur.', 'warning')
            return render_template('auth/connexion.html')

        # ── Connexion réussie ──────────────────────────────────
        login_user(user)
        flash(f'Bienvenue {user.prenom} !', 'success')

        # Rediriger vers la page demandée avant l'interception @login_required
        # Ex : l'utilisateur essayait d'accéder à /profil → il est renvoyé là après connexion
        next_page = request.args.get('next')

        # TODO Branche 04 : remplacer tableau_de_bord par profil.voir_profil
        return redirect(next_page or url_for('auth.tableau_de_bord'))

    return render_template('auth/connexion.html')


# =============================================================
# GET /auth/deconnexion
# @login_required → route accessible uniquement si connecté
# =============================================================
@auth_bp.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()   # Vide la session Flask-Login
    flash('Tu as été déconnecté.', 'info')
    return redirect(url_for('auth.connexion'))


# =============================================================
# GET /auth/tableau-de-bord — STUB temporaire Branche 03
# Sera remplacé par la route profil.voir_profil en Branche 04
# =============================================================
@auth_bp.route('/tableau-de-bord')
@login_required
def tableau_de_bord():
    return render_template('dashboard.html')
