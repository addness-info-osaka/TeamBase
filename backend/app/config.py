import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///teamsbase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
