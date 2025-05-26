from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['FINOVAULT_DATA'] = os.environ.get("FINOVAULT_DATA", "/data")

    from .routes import main
    app.register_blueprint(main)
    return app
