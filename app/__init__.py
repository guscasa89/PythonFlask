from flask import Flask
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_user import UserManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap



db = SQLAlchemy()
admin = Admin()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
bootsrap = Bootstrap()


def create_app(config_name='config.py'):

    app = Flask(__name__)

    # lee la config desde el archivo la clse del Config
    app.config.from_pyfile(config_name)
    login_manager.init_app(app)
    db.init_app(app)
    from .restricted.routes import MyAdminIndexView
    admin.init_app(app, index_view=MyAdminIndexView())

    from .auth.models import Votante
    user_manager = UserManager(app, db, Votante)

    # Registro de los Blueprints
    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .restricted import restricted_bp
    app.register_blueprint(restricted_bp)

    mail.init_app(app)

    migrate.init_app(app, db)

    bootsrap.init_app(app)

    return app






