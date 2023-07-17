from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from os import path
from flask_login import LoginManager

from website.routes.user_bp import user_bp
from website.routes.auth_bp import auth_bp


def create_app():
    app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
    app.config.from_object('config')


    from website.database import db
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='')
    app.register_blueprint(auth_bp, url_prefix='')

    from website.models.models import User, Schedule

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    