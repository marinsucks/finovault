from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['DIR_PATH'] = os.environ.get("DIR_PATH", "/data")
    app.config['DIR_NAME'] = os.environ.get("DIR_NAME", "/data")

    from .routes import main
    app.register_blueprint(main)
    return app
