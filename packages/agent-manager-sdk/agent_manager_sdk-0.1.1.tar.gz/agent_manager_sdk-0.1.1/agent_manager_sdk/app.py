import logging
import os

from app_extensions.celery import init_celery
from app_extensions.db_ext import init_db
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models.account import Account
from models.miniapps.dnd import Chat, User
from models.workflow import Workflow, WorkflowNodeExecution, WorkflowRun

# logging.basicConfig(level=logging.DEBUG)

load_dotenv('secret.env')

migrate = Migrate()


def initialize_extensions(app):
    db = init_db(app)
    migrate.init_app(app, db)   
    init_celery(app)
    
def register_blueprints(app):
    from controllers.console import bp as console_app_bp
    
    app.register_blueprint(console_app_bp)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/dnd_game.db'
    app.config['SQLALCHEMY_BINDS'] = {
    'dnd_db': 'sqlite:///db/dnd_game.db',
}
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', 6379)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=f"redis://{redis_host}:{redis_port}/0",
            result_backend=f"redis://{redis_host}:{redis_port}/0",
            task_ignore_result=True
        )
    )
    
    CORS(app, allow_headers=['Content-Type', 'Authorization', 'ngrok-skip-browser-warning'],
         resources={r"/*": {"origins": "*"}},
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'])
    
    register_blueprints(app)
    initialize_extensions(app)
       
    return app

flask_app = create_app()

# celery_app = flask_app.extensisns['celery']    
if __name__ == '__main__':
    
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
    