"""
config.py
- settings for the flask appobject
"""

class BaseConfig(object):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///smc.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:example@localhost:8089/smc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = 'edifferSMCSystem'