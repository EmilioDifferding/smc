"""
app.py
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_cors import CORS

def create_app(app_name='SMC_API'):
    app = Flask(app_name)
    app.config.from_object('api.config.BaseConfig')
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    from api.api import api
    app.register_blueprint(api, url_prefix="/api")

    from api.botApi import bot
    app.register_blueprint(bot, url_prefix="/api/bot")

    from api.models import db
    db.init_app(app)
    return app