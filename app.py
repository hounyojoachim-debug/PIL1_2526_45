from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
# Clé secrète nécessaire pour gérer les sessions de connexion
app.secret_key = 'mentorlink_secret_key' 

# --- ROUTES D'AUTHENTIFICATION ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # À l'intégration : Vérification BDD ici
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ROUTES DE L'APPLICATION ---

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/edit-profile')
def edit_profile():
    return render_template('edit_profile.html')

if __name__ == '__main__':
    app.run(debug=True)
