from ....app_extensions.db_ext import db


class User(db.Model):
    __bind_key__ = 'dnd_db'
    id = db.Column(db.String, primary_key=True, unique=True)
    chats = db.relationship('Chat', back_populates='user', cascade="all, delete-orphan")