from flask import Blueprint

home_bp = Blueprint('home', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
team_bp = Blueprint('team', __name__)
profiles_bp = Blueprint('profiles', __name__)
categories_bp = Blueprint('categories', __name__)

from app.routes import home, auth, admin, team, profiles, categories
