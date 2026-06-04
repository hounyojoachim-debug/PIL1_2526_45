from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # [Intégration future : Vérification MySQL ici]
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- NOUVELLE ROUTE POUR LA MESSAGERIE ---
@app.route('/messages')
def messages():
    """
    Route de la messagerie : Affiche l'interface de discussion.
    """
    return render_template('messages.html')
# ------------------------------------------

@app.route('/edit-profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
