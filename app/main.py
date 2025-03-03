# main.py
from flask import Flask
from app.config import Config
from web.app import app as web_app

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(web_app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
