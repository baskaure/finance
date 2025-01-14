from datetime import timedelta

class Config:
    SECRET_KEY = 'votre_clé_secrète'  # À changer en production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)