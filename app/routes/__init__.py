from flask import Blueprint

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)

from app.routes import main, auth, admin 