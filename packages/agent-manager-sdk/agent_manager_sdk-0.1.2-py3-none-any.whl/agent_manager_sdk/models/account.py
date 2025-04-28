from enum import Enum

from ..app_extensions.db_ext import db

# from models import StringUUID


class Account(db.Model):
    """
    Account model.
    """
    class AccountType(Enum):
        """
        Account type.
        """
        pass
    
    __tablename__ = 'account'
    __bind_key__ = 'dnd_db'

    user_id = db.Column(db.String, primary_key=True, unique=True)
    # chats = db.relationship('Workflow', back_populates='Account') #, cascade="all, delete-orphan")
    
    
    