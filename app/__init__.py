from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

# Configure SQLAlchemy to work with newer versions
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Debug information
    print("Initializing application...")
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    
    try:
        print("Templates available:", os.listdir(app.template_folder))
    except Exception as e:
        print(f"Error listing templates: {e}")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    # Initialize database and create admin user
    with app.app_context():
        db.create_all()
        from app.models import User
        if User.query.filter_by(username=app.config['ADMIN_USERNAME']).first() is None:
            admin = User(username=app.config['ADMIN_USERNAME'])
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()

    print("Application initialized successfully!")
    return app