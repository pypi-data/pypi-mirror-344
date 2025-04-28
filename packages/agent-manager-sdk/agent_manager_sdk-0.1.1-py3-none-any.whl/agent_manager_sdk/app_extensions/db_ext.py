import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.init_app(app)
        if not os.path.exists('db/dnd_game.db'):
            db.create_all(bind='dnd_db')
    return db
