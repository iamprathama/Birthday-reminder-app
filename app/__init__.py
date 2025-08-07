from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'  # Persistent storage
    app.config['SESSION_PERMANENT'] = False
    
    Session(app)

    db.init_app(app)

    with app.app_context():
        from app import routes
        from app.model import Birthday
        db.create_all()

    return app
