from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    login.init_app(app)

    login.login_view = "auth.login"
    login.login_message_category = "error"
    login.login_message = "Lütfen bu sayfaya erişmek için giriş yapın."

    @login.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500
    
    @app.errorhandler(503)
    def service_unavaible(error):
        return render_template("errors/503.html")
    
    from .routes import home_bp, auth_bp, admin_bp, team_bp, profiles_bp, categories_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(categories_bp)

    return app
