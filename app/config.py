# config.py
import os

class Config:
    """Application configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024 * 1024  # 10GB limit
