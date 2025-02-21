import os
from datetime import timedelta

class Config:
    # Get the folder where this file is located
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Create instance directory if it doesn't exist
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = 'dev-key-please-change-in-production'
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create uploads folder if it doesn't exist
    
    # Admin credentials
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'
    
    # AdSense configuration
    ADSENSE_CLIENT_ID = 'your-adsense-client-id'
    ADSTERRA_ID = 'your-adsterra-id' 