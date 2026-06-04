from flask import Flask
from config import Config
from extensions import db, login_manager, socketio, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    bcrypt.init_app(app)

    from routes.auth       import auth_bp
    from routes.profil     import profil_bp
    from routes.offres     import offres_bp
    from routes.matching   import matching_bp
    from routes.messagerie import messagerie_bp

    app.register_blueprint(auth_bp,        url_prefix='/auth')
    app.register_blueprint(profil_bp,      url_prefix='/profil')
    app.register_blueprint(offres_bp,      url_prefix='/offres')
    app.register_blueprint(matching_bp,    url_prefix='/matching')
    app.register_blueprint(messagerie_bp,  url_prefix='/messagerie')

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
