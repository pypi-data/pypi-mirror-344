from functools import wraps

from flask import abort, current_app, request
from flask_login import current_user
from libs.errors import AccountNotInitializedError


def account_initialization_required(view):
    @wraps(view)
    def decorated(*args, **kwargs):
        # check account initialization
        account = current_user

        if account.status == 'uninitialized':
            raise AccountNotInitializedError()

        return view(*args, **kwargs)

    return decorated