from ....app_extensions.db_ext import db


class Chat(db.Model):
    __bind_key__ = 'dnd_db'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.String)
    player_class = db.Column(db.String)
    player_race = db.Column(db.String)
    player_name = db.Column(db.String)
    player_area = db.Column(db.String)
    player_attributes = db.Column(db.String)
    summaries = db.Column(db.PickleType)
    ai_history = db.Column(db.PickleType)
    user_history = db.Column(db.PickleType)
    
    user = db.relationship('User', back_populates='chats')