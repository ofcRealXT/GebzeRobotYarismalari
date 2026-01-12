from flask import abort
from functools import wraps
import locale
import os

locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

def turkish_datetime(value):
    if not value:
        return ""
    return value.strftime('%d %B %Y, %A %H:%M')

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_login import current_user
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
