from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, template_folder='')
    app.config['SECRET_KEY'] = 'carazinho'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    DATABASE_URL = "postgresql://salaoonline_user:vLkCiPFYWEXDUd3M9DVeNYYBrNXRdkJU@dpg-ciou026nqql4qa0jg33g-a.oregon-postgres.render.com/salaoonline"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Schedule

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app