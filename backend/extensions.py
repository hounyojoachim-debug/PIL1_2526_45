from flask_sqlalchemy import SQLAlchemy
from flask_login    import LoginManager
from flask_socketio import SocketIO
from flask_bcrypt   import Bcrypt

db            = SQLAlchemy()
login_manager = LoginManager()
socketio      = SocketIO()
bcrypt        = Bcrypt()

login_manager.login_view             = 'auth.connexion'
login_manager.login_message          = 'Connecte-toi pour accéder à cette page.'
login_manager.login_message_category = 'info'
