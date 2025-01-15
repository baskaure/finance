from datetime import timedelta

class Config:
    SECRET_KEY = 'votre_clé_secrète' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)