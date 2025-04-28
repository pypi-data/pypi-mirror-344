from flask import Blueprint

from ...app_libs.external_api import ExternalApi

bp = Blueprint('miniapps', __name__, url_prefix='/miniapps')
api = ExternalApi(bp)

# from .app.search import AgentFactory, MichaelScottPackageManager
from .app.workflow import DraftWorkflowApi, DraftWorkflowRunApi
from .miniapps.dnd.endpoints import GenerateMasterPromptAPI
