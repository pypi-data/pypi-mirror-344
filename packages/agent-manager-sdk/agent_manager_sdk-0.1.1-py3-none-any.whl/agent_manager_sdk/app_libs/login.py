from functools import wraps

from flask import current_app, g, has_request_context
from werkzeug.local import LocalProxy

current_user = LocalProxy(lambda: _get_user())

def login_required(func):
    
    @wraps
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        return current_app.login_manager.unauthorized()

def _get_user():
    if has_request_context():
        if "_login_user" not in g:
            current_app.login_manager._load_user()

        return g._login_user

    return None