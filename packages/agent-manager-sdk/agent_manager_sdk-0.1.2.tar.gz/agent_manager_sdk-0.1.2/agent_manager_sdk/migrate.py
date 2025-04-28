import os

from flask import Flask
from flask_migrate import Migrate

from .app_extensions.db_ext import db, init_db

app = Flask(__name__)
db_path = os.getenv('DND_DB_PATH')
app.config['SQLALCHEMY_BINDS'] = {
    'dnd_db': db_path,
}
init_db(app)
migrate = Migrate(app, db)