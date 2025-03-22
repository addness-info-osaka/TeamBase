from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # CORSの設定
    CORS(app)
    
    # データベースの初期化
    db.init_app(app)
    
    # データベースの作成
    with app.app_context():
        db.create_all()
    
    return app
